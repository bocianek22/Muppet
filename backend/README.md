# Backend Muppet AI (orkiestrator)

Zarządzany backend (FastAPI), który: uwierzytelnia urządzenia, trzyma klucze API
(licencja właściciela), orkiestruje tor AI (baza OpenAI / premium Claude+ElevenLabs),
przechowuje presety i pamięć oraz udostępnia REST dla aplikacji mobilnej.

## Uruchomienie (dev)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # wpisz klucze wg trybu (patrz niżej)
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Tryby dostawcy

- `DEFAULT_PROVIDER_PROFILE=base` — wszystko na jednym kluczu **OpenAI**
  (`OPENAI_API_KEY`).
- `DEFAULT_PROVIDER_PROFILE=premium` — **Claude** (mózg, `ANTHROPIC_API_KEY`) +
  **ElevenLabs** (głos, `ELEVENLABS_API_KEY`) + STT OpenAI (`OPENAI_API_KEY`).

Profil można nadpisać per-urządzenie/per-preset (pole `provider_profile`).

## Protokół WSS urządzenia (`/v1/device/ws`)

Nagłówek: `Authorization: Bearer <device_token>` (dev: token = `device_id`).

Urządzenie → backend:
- ramki **binarne** = audio z mikrofonu (PCM16 mono, `AUDIO_SAMPLE_RATE`),
- `{"type":"audio_start"}` — początek wypowiedzi (czyści bufor),
- `{"type":"audio_end"}` — koniec wypowiedzi (uruchamia przetwarzanie),
- `{"type":"hello"}` — poproś o aktualny profil,
- `{"type":"ping"}` — keepalive.

Backend → urządzenie:
- `{"type":"state","value":"transcribing|thinking|idle"}`,
- `{"type":"transcript","role":"user|assistant","text":"..."}`,
- `{"type":"tts_start","sample_rate":16000}`,
- ramki **binarne** = audio TTS do odtworzenia (PCM16 mono),
- `{"type":"tts_end"}`,
- `{"type":"profile", ...}` — wypchnięcie nowego profilu (np. po zmianie w aplikacji),
- `{"type":"error","message":"..."}`.

## REST (aplikacja) — skrót

Patrz pełny kontrakt w [`docs/06-aplikacja-mobilna.md`](../docs/06-aplikacja-mobilna.md).

- `GET /v1/presets`
- `POST /v1/devices/enroll`
- `GET|PUT /v1/devices/{id}/profile`
- `GET|DELETE /v1/devices/{id}/memory`
- `GET /health`

## Pamięć i presety

- Presety: [`presets/*.json`](presets) (zarządzane przez producenta).
- Pamięć egzemplarza: `DATA_DIR/memory/<device_id>.json`, aktualizowana w tle po
  każdej turze (tani model). W produkcji przenieś do bazy z szyfrowaniem i
  politykami retencji (RODO — patrz [`docs/05-zgodnosc-CE-EN71.md`](../docs/05-zgodnosc-CE-EN71.md)).

## Uwagi produkcyjne

- Zastąp uproszczone auth (token=device_id) podpisanymi tokenami (JWT/OAuth) i
  prawdziwym parowaniem (`enroll_token` → `device_token`).
- Dodaj moderację treści (wejście/wyjście), limity planu, rozliczenia.
- Persystencja: Postgres (profile, pamięć, zużycie) + Redis (sesje).
- TLS/WSS + pinning certyfikatu po stronie urządzenia.
