"""Backend Muppet AI — FastAPI.

- WSS dla urządzenia: /v1/device/ws  (audio + sterowanie + profil)
- REST dla aplikacji: presety, profil, pamięć, parowanie

UWAGA (dev): uwierzytelnianie jest uproszczone — token Bearer = device_id.
W produkcji zastąp JWT/OAuth, bazą danych i właściwym parowaniem (enroll).
"""
from __future__ import annotations

import asyncio
import contextlib

from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)

from .config import get_settings
from .memory import DeviceMemory
from .presets import load_presets
from .profiles import load_raw_profile, resolve_profile, save_raw_profile
from .providers import TurnContext, get_provider
from .providers.claude_elevenlabs import extract_memory

app = FastAPI(title="Muppet AI Backend", version="0.1.0")


@app.get("/health")
async def health() -> dict:
    return {"ok": True}


# ── REST dla aplikacji ──────────────────────────────────────────────────────


def _auth_device(authorization: str | None) -> str:
    """Wyciągnij device_id z nagłówka Bearer (dev: token == device_id)."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Brak/zły token")
    return authorization.split(" ", 1)[1].strip()


@app.get("/v1/presets")
async def presets(language: str | None = None, age: str | None = None) -> list[dict]:
    items = load_presets()
    if language:
        items = [p for p in items if p.get("language") == language]
    if age:
        items = [p for p in items if age in p.get("age_range", "")]
    # Nie zwracaj pełnego promptu systemowego do aplikacji — tylko metadane.
    return [
        {k: v for k, v in p.items() if k != "system_prompt"} for p in items
    ]


@app.post("/v1/devices/enroll")
async def enroll(payload: dict) -> dict:
    """Parowanie: wymień enroll_token na device_token (dev: zwróć device_id)."""
    device_id = payload.get("device_id") or "dev_demo"
    # W produkcji: zweryfikuj enroll_token, utwórz rekord, wydaj podpisany token.
    return {"device_id": device_id, "device_token": device_id}


@app.get("/v1/devices/{device_id}/profile")
async def get_profile(device_id: str, authorization: str | None = Header(None)) -> dict:
    _auth_device(authorization)
    return load_raw_profile(device_id)


@app.put("/v1/devices/{device_id}/profile")
async def put_profile(
    device_id: str, body: dict, authorization: str | None = Header(None)
) -> dict:
    _auth_device(authorization)
    updated = save_raw_profile(device_id, body)
    # Wypchnij nowy profil do urządzenia, jeśli jest podłączone.
    conn = _CONNECTIONS.get(device_id)
    if conn is not None:
        await conn.push_profile()
    return updated


@app.get("/v1/devices/{device_id}/memory")
async def get_memory(device_id: str, authorization: str | None = Header(None)) -> dict:
    _auth_device(authorization)
    return DeviceMemory(device_id).data


@app.delete("/v1/devices/{device_id}/memory")
async def clear_memory(device_id: str, authorization: str | None = Header(None)) -> dict:
    _auth_device(authorization)
    mem = DeviceMemory(device_id)
    mem.clear()
    return {"ok": True}


# ── WSS urządzenia ──────────────────────────────────────────────────────────


class DeviceConnection:
    """Sesja jednego urządzenia: bufor audio, historia, profil, emisja."""

    def __init__(self, ws: WebSocket, device_id: str) -> None:
        self.ws = ws
        self.device_id = device_id
        self.audio_buf = bytearray()
        self.history: list[dict] = []
        self.memory = DeviceMemory(device_id)
        self._busy = False

    async def emit_event(self, event: dict) -> None:
        await self.ws.send_json(event)

    async def emit_audio(self, pcm: bytes) -> None:
        await self.ws.send_bytes(pcm)

    async def push_profile(self) -> None:
        profile = resolve_profile(self.device_id)
        await self.emit_event(
            {
                "type": "profile",
                "preset_id": profile["preset"]["id"],
                "language": profile.get("language"),
                "provider_profile": profile.get("provider_profile"),
            }
        )

    async def handle_turn(self) -> None:
        if self._busy or not self.audio_buf:
            return
        self._busy = True
        audio_in = bytes(self.audio_buf)
        self.audio_buf.clear()
        try:
            profile = resolve_profile(self.device_id)
            provider = get_provider(profile.get("provider_profile", "premium"))
            ctx = TurnContext(
                audio_in=audio_in,
                sample_rate=get_settings().audio_sample_rate,
                profile=profile,
                memory=self.memory,
                history=self.history,
                emit_audio=self.emit_audio,
                emit_event=self.emit_event,
            )
            await provider.respond(ctx)
            # Aktualizacja pamięci w tle (nie blokuje rozmowy).
            asyncio.create_task(extract_memory(self.history, self.memory))
        except Exception as exc:  # noqa: BLE001 — zgłoś błąd urządzeniu, nie wywalaj sesji
            with contextlib.suppress(Exception):
                await self.emit_event({"type": "error", "message": str(exc)})
                await self.emit_event({"type": "state", "value": "idle"})
        finally:
            self._busy = False


_CONNECTIONS: dict[str, DeviceConnection] = {}


@app.websocket("/v1/device/ws")
async def device_ws(ws: WebSocket) -> None:
    # Autoryzacja: nagłówek Authorization: Bearer <device_token>
    auth = ws.headers.get("authorization")
    try:
        device_id = _auth_device(auth)
    except HTTPException:
        await ws.close(code=4401)
        return

    await ws.accept()
    conn = DeviceConnection(ws, device_id)
    _CONNECTIONS[device_id] = conn
    await conn.push_profile()
    await conn.emit_event({"type": "state", "value": "idle"})

    try:
        while True:
            msg = await ws.receive()
            if msg.get("type") == "websocket.disconnect":
                break
            if (data := msg.get("bytes")) is not None:
                # Ramka audio z mikrofonu (PCM16 mono).
                conn.audio_buf.extend(data)
            elif (text := msg.get("text")) is not None:
                event = _safe_json(text)
                etype = event.get("type")
                if etype == "audio_start":
                    conn.audio_buf.clear()
                elif etype == "audio_end":
                    # Przetwórz turę (osobny task, by dalej odbierać sterowanie).
                    asyncio.create_task(conn.handle_turn())
                elif etype == "hello":
                    await conn.push_profile()
                elif etype == "ping":
                    await conn.emit_event({"type": "pong"})
    except WebSocketDisconnect:
        pass
    finally:
        _CONNECTIONS.pop(device_id, None)


def _safe_json(text: str) -> dict:
    import json

    try:
        out = json.loads(text)
        return out if isinstance(out, dict) else {}
    except json.JSONDecodeError:
        return {}
