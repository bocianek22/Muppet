# Agent urządzenia (Raspberry Pi)

Cienki klient na Raspberry Pi Zero 2 W: nagrywa mowę, strumieniuje do backendu,
odtwarza odpowiedź głosową i **rusza buzią** maskotki (serwo) w rytm dźwięku.
Cała logika AI jest w backendzie — agent zajmuje się tylko audio, sterowaniem i
łącznością.

## Wymagania systemowe

- Raspberry Pi OS Lite (64-bit), I2S włączone (mikrofon INMP441 + wzmacniacz
  MAX98357A) — patrz [`docs/03-schemat-polaczen.md`](../docs/03-schemat-polaczen.md)
  i [`docs/04-montaz-i-uruchomienie.md`](../docs/04-montaz-i-uruchomienie.md).
- Pakiety: `python3-venv`, `libportaudio2` (dla sounddevice).

## Instalacja

```bash
sudo apt install -y python3-venv libportaudio2
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yaml config.yaml   # uzupełnij backend_url, device_token, piny
python -m muppet_agent.main --config config.yaml
```

Autostart (systemd): patrz [`systemd/muppet-agent.service`](systemd/muppet-agent.service)
i [`docs/04-montaz-i-uruchomienie.md`](../docs/04-montaz-i-uruchomienie.md).

## Sterowanie buzią i diodą

- Serwo (`pins.servo`) otwiera/zamyka buzię proporcjonalnie do głośności
  odtwarzanego dźwięku (RMS bloku audio). Parametry w `config.yaml` (`mouth`).
- Dioda (`pins.led`) sygnalizuje stan: nasłuch / myślenie / mówienie / błąd.
- Dla płynnego PWM serwa zalecany `pigpio` (`sudo pigpiod`, `GPIOZERO_PIN_FACTORY=pigpio`).

## Tryb wejścia

- `push_to_talk: true` — nagrywanie tylko z wciśniętym przyciskiem (domyślne;
  zgodne z wytycznymi prywatności — urządzenie nie nasłuchuje stale).
- `push_to_talk: false` — miejsce na wake-word / VAD (do rozbudowy). Dla dzieci
  rekomendowane jest jednak push-to-talk + wyraźna dioda nasłuchu.

## Parowanie i WiFi (BLE provisioning)

Zaimplementowane w [`muppet_agent/provisioning.py`](muppet_agent/provisioning.py)
(serwer GATT na BlueZ przez bibliotekę `bless`). Gdy `device_token` jest pusty lub
równy `dev_demo`, agent **automatycznie wchodzi w tryb parowania** przy starcie
(można też wymusić flagą `--provision`).

Przepływ:
1. Urządzenie rozgłasza usługę GATT (`Muppet-Setup`) z charakterystykami:
   `wifi_ssid`, `wifi_pass`, `enroll_token` (write), `command` (write, `commit`),
   `status` (read/notify).
2. Aplikacja zapisuje dane sieci + `enroll_token`, następnie `command="commit"`.
3. Urządzenie łączy WiFi (`nmcli`), wymienia `enroll_token` → `device_token`
   (REST `POST /v1/devices/enroll`), zapisuje `config.yaml`, zgłasza `online`.
4. Tryb parowania kończy się, agent przechodzi do normalnej pracy.

UUID-y i kontrakt: [`docs/06-aplikacja-mobilna.md`](../docs/06-aplikacja-mobilna.md).
Wymaga BlueZ; poza Pi (dev) moduł grzecznie pomija parowanie.

> Uwaga produkcyjna: hasło WiFi i token przesyłaj po **zaszyfrowanym** połączeniu
> BLE (parowanie/bonding), a `enroll_token` traktuj jako jednorazowy i krótkożyciowy.
