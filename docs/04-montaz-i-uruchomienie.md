# 04 — Montaż i uruchomienie

## 1. Montaż elektroniki

1. Połącz moduły wg [`docs/03-schemat-polaczen.md`](03-schemat-polaczen.md).
2. Zasilanie: akumulator → moduł ładowarka/boost 5 V → szyna 5 V/GND. Sprawdź
   napięcia **przed** podpięciem Pi.
3. Dodaj kondensator (470–1000 µF) blisko serwa (skoki prądu).
4. Zamknij elektronikę i akumulator w komorze **na śrubę** (wymóg EN 71 — patrz
   [`docs/05-zgodnosc-CE-EN71.md`](05-zgodnosc-CE-EN71.md)).

## 2. Przygotowanie systemu na Raspberry Pi

1. Nagraj **Raspberry Pi OS Lite (64-bit)** na microSD (Raspberry Pi Imager).
   W ustawieniach Imagera ustaw hostname, SSH, użytkownika (na czas dev).
2. Włącz I2S — w `/boot/firmware/config.txt`:
   ```ini
   dtparam=i2s=on
   dtparam=audio=off
   dtoverlay=max98357a,sdmode-pin=4
   dtoverlay=googlevoicehat-soundcard
   ```
   (overlaye zależą od jądra — patrz uwagi w doc 03).
3. Po starcie sprawdź urządzenia audio:
   ```bash
   aplay -l     # powinien być MAX98357A (playback)
   arecord -l   # powinien być mikrofon I2S (capture)
   ```

## 3. Instalacja agenta urządzenia

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip libatlas-base-dev
git clone <repo> muppet && cd muppet/device
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yaml config.yaml
# uzupełnij config.yaml: adres backendu, identyfikatory, piny
```

Uruchomienie testowe:

```bash
python -m muppet_agent.main --config config.yaml
```

Jako usługa systemd (autostart):

```bash
sudo cp systemd/muppet-agent.service /etc/systemd/system/
sudo systemctl enable --now muppet-agent
journalctl -u muppet-agent -f   # logi
```

> W produkcie WiFi konfiguruje się przez aplikację (BLE provisioning), a
> `device_token` urządzenie dostaje przy rejestracji — patrz
> [`docs/06-aplikacja-mobilna.md`](06-aplikacja-mobilna.md). Na etapie dev można
> wpisać dane do `config.yaml`.

## 4. Uruchomienie backendu (dewelopersko)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# wpisz klucze: ANTHROPIC_API_KEY, OPENAI_API_KEY, ELEVENLABS_API_KEY (wg trybu)
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Szczegóły, zmienne i protokół WSS: [`backend/README.md`](../backend/README.md).

## 5. Aplikacja mobilna (dewelopersko)

```bash
cd app
npm install
npx expo start
```

Szczegóły i kontrakt API: [`app/README.md`](../app/README.md) oraz
[`docs/06-aplikacja-mobilna.md`](06-aplikacja-mobilna.md).

## 6. Pierwsze uruchomienie (ścieżka klienta)

1. Włącz maskotkę (dioda: tryb parowania).
2. W aplikacji: zaloguj się → „Dodaj urządzenie" → wybierz sieć WiFi → wpisz hasło.
3. Aplikacja przez BLE przekazuje dane; urządzenie łączy się i rejestruje.
4. Wybierz charakter, ewentualnie dostrój styl.
5. Naciśnij przycisk na maskotce (push-to-talk) i rozmawiaj.

## 7. Diagnostyka

| Objaw | Sprawdź |
|---|---|
| Brak dźwięku | `aplay -l`, połączenia I2S DOUT/BCLK/LRCLK, zasilanie MAX98357A |
| Brak nagrywania | `arecord -l`, INMP441 SD/WS/SCK, L/R do GND |
| Serwo nie rusza | zasilanie 5 V serwa (nie z 3V3), wspólna masa, pin PWM |
| Brak połączenia | WiFi, adres backendu, `device_token`, certyfikat TLS |
| Wysoka latencja | tryb providera (baza vs premium), jakość WiFi, region serwera |
