"""Parowanie urządzenia przez BLE (provisioning WiFi + rejestracja w backendzie).

Urządzenie w trybie parowania uruchamia serwer GATT (peryferyjne BLE), z którego
aplikacja mobilna odczytuje status i zapisuje dane sieci oraz token rejestracyjny.
Po komendzie "commit" urządzenie:
  1) zapisuje WiFi (nmcli — NetworkManager, domyślny na Raspberry Pi OS Bookworm),
  2) wymienia enroll_token -> device_token w backendzie (REST /v1/devices/enroll),
  3) zapisuje wynik do config.yaml i kończy tryb parowania.

Kontrakt GATT (UUID-y poniżej) — zgodny z docs/06-aplikacja-mobilna.md:
  wifi_ssid    (write)
  wifi_pass    (write)
  enroll_token (write)
  command      (write)   — "commit"
  status       (read/notify) — provisioning|connecting|enrolling|online|error:<kod>

Moduł działa na Raspberry Pi z BlueZ (biblioteka `bless`). Bez BLE (np. na
komputerze deweloperskim) przechodzi w tryb zaślepki, by nie blokować rozwoju.
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import urllib.request

import yaml

# UUID-y usługi i charakterystyk (stałe dla całego produktu).
SERVICE_UUID = "6d757070-6574-0001-0000-000000000000"
CHAR_SSID = "6d757070-6574-0001-0001-000000000000"
CHAR_PASS = "6d757070-6574-0001-0002-000000000000"
CHAR_ENROLL = "6d757070-6574-0001-0003-000000000000"
CHAR_COMMAND = "6d757070-6574-0001-0004-000000000000"
CHAR_STATUS = "6d757070-6574-0001-0005-000000000000"

try:
    from bless import (  # type: ignore
        BlessServer,
        GATTAttributePermissions,
        GATTCharacteristicProperties,
    )

    _HAS_BLE = True
except Exception:  # noqa: BLE001 — środowisko bez BLE/BlueZ
    _HAS_BLE = False


def needs_provisioning(config: dict) -> bool:
    """Czy urządzenie wymaga parowania (brak realnego tokenu/sieci)."""
    token = (config.get("device_token") or "").strip()
    return token in ("", "dev_demo", "ZASTAP")


def _api_base(config: dict) -> str:
    """Wyprowadź bazowy URL HTTP API z ustawień (do enrollu)."""
    if config.get("api_base_url"):
        return config["api_base_url"].rstrip("/")
    # Z backend_url (ws[s]://host/v1/device/ws) zrób http[s]://host/v1
    url = config.get("backend_url", "")
    url = url.replace("wss://", "https://").replace("ws://", "http://")
    return url.split("/v1/")[0].rstrip("/") + "/v1"


def apply_wifi(ssid: str, password: str) -> None:
    """Skonfiguruj i połącz WiFi (NetworkManager)."""
    subprocess.run(
        ["nmcli", "dev", "wifi", "connect", ssid, "password", password],
        check=True,
        capture_output=True,
        timeout=45,
    )


def enroll(api_base: str, enroll_token: str, device_hint: str) -> str:
    """Wymień enroll_token na trwały device_token w backendzie."""
    body = json.dumps({"enroll_token": enroll_token, "device_id": device_hint}).encode()
    req = urllib.request.Request(
        f"{api_base}/devices/enroll",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310 — własny backend
        data = json.loads(resp.read().decode())
    return data["device_token"]


def save_config(config_path: str, config: dict, device_token: str) -> None:
    config = dict(config)
    config["device_token"] = device_token
    with open(config_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(config, fh, allow_unicode=True, sort_keys=False)


async def run_provisioning(config: dict, config_path: str) -> dict:
    """Uruchom tryb parowania; zwróć zaktualizowany config (z device_token).

    Bez BLE (dev) zwraca config bez zmian (parowanie pomijane).
    """
    if not _HAS_BLE:
        print("[provisioning] BLE niedostępne — pomijam (tryb dev).")
        return config

    loop = asyncio.get_event_loop()
    collected: dict[str, str] = {}
    done = asyncio.Event()
    result: dict = {}

    server = BlessServer(name=config.get("provisioning", {}).get("service_name", "Muppet-Setup"), loop=loop)

    def _set_status(value: str) -> None:
        char = server.get_characteristic(CHAR_STATUS)
        if char is not None:
            char.value = value.encode()
            server.update_value(SERVICE_UUID, CHAR_STATUS)

    def read_cb(characteristic, **_):  # noqa: ANN001
        return characteristic.value

    def write_cb(characteristic, value, **_):  # noqa: ANN001
        uuid = characteristic.uuid.lower()
        text = bytes(value).decode(errors="ignore")
        if uuid == CHAR_SSID:
            collected["ssid"] = text
        elif uuid == CHAR_PASS:
            collected["pass"] = text
        elif uuid == CHAR_ENROLL:
            collected["enroll"] = text
        elif uuid == CHAR_COMMAND and text.strip() == "commit":
            loop.create_task(_commit())

    async def _commit() -> None:
        try:
            _set_status("connecting")
            await loop.run_in_executor(
                None, apply_wifi, collected.get("ssid", ""), collected.get("pass", "")
            )
            _set_status("enrolling")
            token = await loop.run_in_executor(
                None,
                enroll,
                _api_base(config),
                collected.get("enroll", ""),
                config.get("device_token") or "dev",
            )
            save_config(config_path, config, token)
            result["device_token"] = token
            _set_status("online")
            done.set()
        except subprocess.CalledProcessError:
            _set_status("error:wifi")
        except Exception as exc:  # noqa: BLE001
            _set_status(f"error:{type(exc).__name__}")

    # Definicja usługi + charakterystyk
    server.read_request_func = read_cb
    server.write_request_func = write_cb
    await server.add_new_service(SERVICE_UUID)

    write_props = GATTCharacteristicProperties.write
    write_perms = GATTAttributePermissions.writeable
    for uuid in (CHAR_SSID, CHAR_PASS, CHAR_ENROLL, CHAR_COMMAND):
        await server.add_new_characteristic(SERVICE_UUID, uuid, write_props, None, write_perms)

    status_props = GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify
    status_perms = GATTAttributePermissions.readable
    await server.add_new_characteristic(
        SERVICE_UUID, CHAR_STATUS, status_props, b"provisioning", status_perms
    )

    await server.start()
    print("[provisioning] tryb parowania aktywny — czekam na aplikację...")
    try:
        await done.wait()
    finally:
        await server.stop()

    config = dict(config)
    config["device_token"] = result.get("device_token", config.get("device_token"))
    return config
