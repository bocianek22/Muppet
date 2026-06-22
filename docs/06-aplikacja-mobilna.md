# 06 — Aplikacja mobilna, presety i kontrakt API

Aplikacja (iOS/Android) jest jedynym interfejsem konfiguracyjnym dla klienta.
Cel: **zero technicznej konfiguracji** — parowanie WiFi przez Bluetooth, wybór
charakteru, gotowe.

## 1. Główne ekrany / przepływy

1. **Onboarding / konto** — rejestracja/logowanie (email lub OAuth), zgody RODO
   (w tym zgoda rodzica na dane dziecka), wybór planu (abonament / „własny klucz").
2. **Parowanie urządzenia (provisioning)**:
   - Aplikacja łączy się z maskotką przez **BLE** (urządzenie rozgłasza usługę
     konfiguracyjną w trybie parowania — dioda sygnalizuje).
   - Aplikacja przesyła: SSID + hasło WiFi oraz **token rejestracyjny** konta.
   - Urządzenie łączy się z WiFi, rejestruje w backendzie, otrzymuje
     `device_token`. Status wraca do aplikacji.
3. **Wybór charakteru (preset)** — galeria gotowych charakterów (patrz §3) z
   opisem, próbką głosu i tagiem wieku. Jeden tap = aktywacja.
4. **Dostrajanie** — suwaki/przełączniki: energia, humor, gadatliwość, język,
   tempo mowy; pole „dodatkowe wskazówki" (free-text dołączane do promptu).
5. **Kontrola rodzicielska** — limity czasu, blokady tematów, godziny ciszy,
   podgląd transkryptów, przycisk „wyczyść pamięć", włącz/wyłącz historię.
6. **Historia / pamięć** — co maskotka zapamiętała (imię, preferencje), z opcją
   edycji i usunięcia (RODO).
7. **Ustawienia urządzenia** — głośność (z górnym limitem), aktualizacje (OTA),
   tryb własnego klucza API, stan akumulatora, reset.

## 2. Onboarding BLE — kontrakt (poglądowy)

Usługa GATT urządzenia w trybie parowania:

- Charakterystyka `wifi_ssid` (write)
- Charakterystyka `wifi_pass` (write, szyfrowane)
- Charakterystyka `enroll_token` (write) — token z konta klienta
- Charakterystyka `status` (notify) — `provisioning|connecting|online|error:<kod>`

Po sukcesie urządzenie wymienia `enroll_token` na trwały `device_token` w
backendzie (endpoint `/v1/devices/enroll`) i łączy się przez WSS.

## 3. Presety / charaktery

Preset to plik JSON (źródło: [`backend/presets/`](../backend/presets)) zarządzany
przez producenta i serwowany do aplikacji. Klient wybiera, a personalizacja
egzemplarza (pamięć) rozwija charakter dalej.

Schemat presetu:

```json
{
  "id": "wesoly-bajkopisarz",
  "name": "Wesoły Bajkopisarz",
  "description": "Opowiada bajki, śpiewa, zadaje zagadki.",
  "age_range": "3-7",
  "language": "pl",
  "system_prompt": "Jesteś ciepłą, wesołą maskotką dla dzieci...",
  "style": { "energy": 0.8, "humor": 0.7, "verbosity": 0.4, "speaking_rate": 1.0 },
  "voice": {
    "provider": "elevenlabs",
    "voice_id": "<id_glosu>",
    "model": "eleven_flash_v2_5",
    "openai_realtime_voice": "alloy"
  },
  "safety": {
    "max_age_content": "kids",
    "blocked_topics": ["przemoc", "treści dla dorosłych", "leki"],
    "refusal_style": "łagodnie zmień temat i zaproponuj zabawę"
  },
  "provider_profile": "base"
}
```

`provider_profile`: `base` (OpenAI Realtime) lub `premium` (Claude+ElevenLabs).
Aplikacja może to nadpisać zależnie od planu klienta.

## 4. Kontrakt API backendu (dla aplikacji)

Bazowy URL: `https://api.<twoja-domena>/v1`. Autoryzacja: `Authorization: Bearer
<jwt_użytkownika>`.

| Metoda | Ścieżka | Opis |
|---|---|---|
| `POST` | `/auth/register`, `/auth/login` | Konto, JWT |
| `POST` | `/devices/enroll` | Wymiana `enroll_token` → rejestracja urządzenia |
| `GET`  | `/devices` | Lista urządzeń użytkownika + status/akumulator |
| `GET`  | `/presets` | Galeria charakterów (filtr: język, wiek) |
| `GET`  | `/devices/{id}/profile` | Aktywny preset + dostrojenia + ustawienia |
| `PUT`  | `/devices/{id}/profile` | Zmień preset / styl / język / głos |
| `GET`  | `/devices/{id}/memory` | Co maskotka zapamiętała |
| `DELETE` | `/devices/{id}/memory` | Wyczyść pamięć (RODO) |
| `GET`  | `/devices/{id}/history` | Transkrypty (jeśli włączone) |
| `PUT`  | `/devices/{id}/parental` | Limity czasu, blokady, godziny ciszy |
| `PUT`  | `/devices/{id}/byok` | Ustaw własny klucz API (tryb hybrydowy) |
| `GET`  | `/devices/{id}/usage` | Zużycie/limity planu |

Przykład zmiany profilu:

```http
PUT /v1/devices/dev_123/profile
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "preset_id": "spokojny-medrzec",
  "style": { "verbosity": 0.6, "speaking_rate": 0.95 },
  "language": "pl",
  "provider_profile": "premium"
}
```

Backend wypycha nowy profil do urządzenia natychmiast (kanał WSS), więc zmiana
charakteru działa „od ręki", bez restartu.

## 5. Połączenie urządzenie ↔ backend (WSS)

Urządzenie utrzymuje stałe połączenie `wss://api.<domena>/v1/device/ws` z
nagłówkiem `Authorization: Bearer <device_token>`. Protokół wiadomości opisany w
[`backend/README.md`](../backend/README.md) i zaimplementowany w
[`device/`](../device).

## 6. Stack aplikacji (rekomendacja)

- **Expo / React Native** (jeden kod na iOS+Android), `react-native-ble-plx`
  do BLE, ekrany w [`app/`](../app).
- Alternatywnie Flutter — kontrakt API jest taki sam.

Szkielet i instrukcja: [`app/README.md`](../app/README.md).
