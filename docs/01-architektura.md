# 01 — Architektura systemu

## 1. Przegląd

System składa się z trzech elementów, którymi zarządza producent, oraz dostawców
AI „pod spodem":

1. **Urządzenie (maskotka)** — Raspberry Pi Zero 2 W (docelowo CM4) z audio I/O,
   serwem ruchu buzi, akumulatorem i diodą stanu. Uruchamia *agenta* (Python),
   który łączy się z naszym backendem przez bezpieczny WebSocket (WSS).
2. **Backend (chmura producenta)** — FastAPI. Uwierzytelnia urządzenia, trzyma
   klucze API, orkiestruje tor AI, przechowuje presety i pamięć, moderuje treść,
   obsługuje abonament/rozliczenia oraz API dla aplikacji.
3. **Aplikacja mobilna** — onboarding WiFi (BLE), wybór charakteru, dostrajanie
   stylu, historia, kontrola rodzicielska, konto.

Dostawcy AI:

- **Baza (1 licencja):** OpenAI Realtime API (mowa→rozum→mowa w jednym strumieniu).
- **Premium:** rozum = Anthropic **Claude**, głos = **ElevenLabs**; opcjonalnie
  **Gemini Live**. Wybór per-urządzenie/per-preset, sterowany z backendu.

## 2. Dlaczego taki podział

| Decyzja | Uzasadnienie |
|---|---|
| Cała AI w chmurze | Tani mikrokontroler/Pi wystarcza; jakość zależy od modeli; klucze nie wyciekają z urządzenia. |
| Backend producenta (hybryda) | Klient nie stawia serwerów; my zarządzamy licencjami i abonamentem; zaawansowani mogą wpiąć własny klucz. |
| Provider abstraction | „Jedna licencja" (OpenAI Realtime) jako baza, przełączenie na Claude+ElevenLabs bez zmiany firmware'u. |
| Raspberry Pi w środku | Linux = proste parowanie BLE, OTA, wake-word, pełne SDK; „kompletny produkt". |
| Streaming zdanie-po-zdaniu | Maskotka zaczyna mówić zanim cała odpowiedź powstanie → naturalna rozmowa. |

## 3. Tryby pracy toru AI

### 3.1 Tryb BAZOWY — OpenAI Realtime (rekomendowany start)

Jeden klucz, jeden strumień. Urządzenie wysyła PCM z mikrofonu, backend
pośredniczy do OpenAI Realtime (przez WebRTC/WebSocket), a wygenerowany głos
wraca strumieniowo do urządzenia. Najniższa latencja (~300–800 ms do pierwszego
dźwięku), najprostsza integracja, najtańszy start.

```
Mic PCM ─► Pi agent ─► Backend ─► OpenAI Realtime (STT+LLM+TTS) ─► Backend ─► Pi ─► głośnik
```

### 3.2 Tryb PREMIUM — Claude + ElevenLabs (potok)

```
Mic PCM ─► Pi ─► Backend ─┬─► STT (OpenAI Whisper / ElevenLabs Scribe) ─► tekst
                          │
                          ├─► Claude (mózg, streaming) ─► zdania ─┐
                          │                                       │
                          └─► ElevenLabs TTS (per zdanie) ◄───────┘ ─► PCM ─► Pi ─► głośnik
```

Najlepsza jakość rozumowania (Claude) i najnaturalniejszy/klonowalny głos
(ElevenLabs). Wyższa latencja niż realtime, ale backend tnie ją strumieniując
odpowiedź Claude zdanie po zdaniu wprost do TTS.

> Wybór modelu Claude: domyślnie `claude-opus-4-8`. Dla maksymalnie niskiej
> latencji w zabawce można w konfiguracji przełączyć na `claude-haiku-4-5` lub
> `claude-sonnet-4-6` — to świadoma decyzja właściciela (kompromis jakość/koszt/szybkość).

### 3.3 Opcjonalnie — Gemini Live

Alternatywa speech-to-speech na jednym kluczu Google. Podpięta przez tę samą
abstrakcję dostawców (`backend/app/providers/`).

## 4. Przepływ rozmowy (sekwencja)

```
Użytkownik          Urządzenie (Pi)        Backend                 Dostawca AI
   │   mówi             │                      │                        │
   │ ─── push/wake ───► │ start nagrywania     │                        │
   │                    │ ── audio frames ───► │ ── strumień audio ───► │
   │                    │   (PCM16 16 kHz)     │   (moderacja wejścia)  │
   │                    │ ── "koniec mowy" ──► │ ── (VAD/EOS) ────────► │
   │                    │                      │   STT → LLM → TTS      │
   │                    │ ◄── audio TTS ────── │ ◄── audio/tekst ────── │
   │ ◄── głos + buzia   │  (serwo wg amplit.)  │   (zapis do pamięci)   │
```

## 5. Pamięć i personalizacja

- **Preset (charakter)** — szablon producenta: prompt systemowy, głos, styl,
  granice, wiek. Wybierany w aplikacji. Format: [`backend/presets/`](../backend/presets).
- **Pamięć egzemplarza** — per `device_id`: imię dziecka, preferencje, wątki
  rozmów, „co lubi maskotka". Wstrzykiwana do kontekstu modelu, dzięki czemu
  charakter **rozwija się** z czasem. Przechowywana po stronie backendu (RODO!).
- **Profil** = preset + pamięć + ustawienia rodzica (limity czasu, tematy).

## 6. Bezpieczeństwo i prywatność (skrót, szczegóły w doc 05)

- Urządzenie uwierzytelnia się tokenem urządzenia (provisioning podczas parowania).
- Transport: TLS/WSS, certyfikat przypięty (pinning) w agencie.
- Moderacja treści na wejściu i wyjściu (Moderation API + reguły presetu wieku).
- Dane głosowe: minimalna retencja, możliwość wyłączenia historii, zgody RODO.
- Kontrola rodzicielska: limity czasu, blokady tematów, podgląd transkryptów.

## 7. Latencja — budżet i optymalizacje

| Etap | Baza (Realtime) | Premium (potok) |
|---|---|---|
| Mic → backend (WiFi) | 20–60 ms | 20–60 ms |
| STT | (w strumieniu) | 150–400 ms |
| LLM pierwszy token | 200–500 ms | 250–600 ms |
| TTS pierwszy dźwięk | (w strumieniu) | 150–400 ms |
| Backend → głośnik | 20–60 ms | 20–60 ms |
| **Razem (pierwszy dźwięk)** | **~0.3–0.8 s** | **~0.8–1.8 s** |

Optymalizacje: VAD na urządzeniu, strumieniowanie zdań, prompt caching (Claude),
TTS o niskiej latencji (ElevenLabs Flash / model realtime), bufor odtwarzania.

## 8. Koszty operacyjne (orientacyjnie)

Koszty zależą od dostawcy i intensywności rozmów. Przyjmując ~10 min rozmowy
dziennie:

- **Baza (OpenAI Realtime):** dominują koszty audio in/out — rząd kilku–
  kilkunastu USD/mies. na aktywne urządzenie.
- **Premium (Claude+ElevenLabs):** koszt = tokeny Claude + znaki ElevenLabs +
  STT. Prompt caching mocno obniża koszt Claude przy stałym prompcie systemowym.

W modelu hybrydowym koszt pokrywa abonament (zarządzany) albo klient (własny
klucz). Backend liczy zużycie per-urządzenie i egzekwuje limity planu.

## 9. Skalowanie produkcyjne

- **Compute:** Pi Zero 2 W na start i małe serie; **CM4 + własna płyta nośna**
  przy większej skali (dostępność długoterminowa, łatwiejsza certyfikacja,
  integracja zasilania/audio na jednej PCB). Patrz [BOM](02-lista-czesci-BOM.md).
- **Backend:** bezstanowe instancje FastAPI za load-balancerem; baza (Postgres)
  na profile/pamięć/rozliczenia; Redis na sesje; kolejki na zdarzenia.
- **OTA:** aktualizacje agenta i modeli z poziomu backendu, bez wizyty serwisu.

## 10. Wariant ultra-tani (opcjonalny) — ESP32-S3

Dla wariantu „cienki klient" zamiast Pi można użyć ESP32-S3 (audio I2S, WiFi,
~5 USD klon). Logika AI i tak jest w chmurze, więc protokół WSS pozostaje ten
sam. Minusy: brak Linuksa (trudniejsze OTA/parowanie/wake-word). Traktujemy to
jako przyszłą linię „lite", nie podstawę produktu.
