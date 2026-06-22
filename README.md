# Muppet AI — gadająca maskotka z konwersacją na żywo

Kompletny, gotowy do produkcji projekt maskotki typu *muppet*, która prowadzi
**rozmowę głosową na żywo** z człowiekiem — w stylu robotów Unitree — w oparciu o
popularne modele AI. Produkt jest **kompletny i prosty w obsłudze**: klient kupuje
urządzenie, instaluje aplikację na telefonie, wybiera charakter maskotki i zaczyna
rozmawiać. Żadnego stawiania serwerów ani grzebania w kodzie.

## Co dostaje klient

- **Gotowe urządzenie** z wbudowanym komputerem (Raspberry Pi Zero 2 W, docelowo
  moduł CM4 przy produkcji seryjnej), mikrofonem, głośnikiem, akumulatorem i
  serwomechanizmem ruchu buzi — wszystko w głowie maskotki.
- **Aplikację mobilną** (iOS/Android) do: parowania z WiFi (Bluetooth, bez
  klawiatury na urządzeniu), wyboru **charakteru/presetu** maskotki, dostrajania
  stylu rozmowy, podglądu historii i kontroli rodzicielskiej.
- **Zarządzaną usługę w chmurze** (model **hybrydowy**): domyślnie abonament z
  wliczonym kosztem AI (klient nic nie konfiguruje), z opcją wpisania **własnego
  klucza API** dla zaawansowanych.

## Architektura (skrót)

```
 ┌─────────────────────────┐     WSS      ┌───────────────────────────┐
 │   MASKOTKA (urządzenie)  │◄────────────►│   BACKEND (nasz, w chmurze)│
 │  Raspberry Pi Zero 2 W   │   audio +    │  - uwierzytelnianie urządz.│
 │  mikrofon I2S            │   sterowanie │  - presety/charaktery       │
 │  wzmacniacz + głośnik    │              │  - pamięć długoterminowa    │
 │  serwo (ruch buzi)       │              │  - abstrakcja dostawców AI ─┼─► OpenAI Realtime (baza, 1 klucz)
 │  akumulator + ładowanie  │              │  - moderacja treści         │   └─► Claude + ElevenLabs (premium)
 │  przycisk + LED          │              │  - rozliczenia/abonament     │       (+opcjonalnie Gemini Live)
 └─────────────────────────┘              └───────────────┬───────────┘
            ▲                                              │  REST/Realtime
            │ BLE provisioning                             ▼
       ┌────┴───────────┐                         ┌────────────────┐
       │ APLIKACJA (tel.)│◄───────────────────────►│   Konto klienta │
       └─────────────────┘     REST/WebSocket      └────────────────┘
```

**Tryb bazowy „na jednej licencji"**: cały tor mowa→rozum→mowa realizuje jeden
dostawca (OpenAI Realtime) — najniższa latencja i najprostsza integracja.
**Tryb premium**: rozum = **Claude**, głos = **ElevenLabs** (najnaturalniejszy,
możliwość klonowania głosu), z opcjonalnym **Gemini Live**. Przełączenie odbywa
się po stronie backendu — bez zmiany firmware'u.

Dlaczego całe przetwarzanie AI jest w chmurze, a nie na urządzeniu:

- **Bezpieczeństwo licencji** — klucze API nigdy nie trafiają na urządzenie.
- **Prostota dla klienta** — zero konfiguracji, automatyczne aktualizacje modeli.
- **Niska latencja i jakość** — backend strumieniuje odpowiedź zdanie po zdaniu do
  syntezatora, a do „myślenia" używa najlepszych modeli niezależnie od taniego
  sprzętu w maskotce.

## Charaktery / presety (kluczowa funkcja)

Charaktery to definiowane **przez nas** szablony osobowości (np. „Wesoły
bajkopisarz", „Spokojny mędrzec", „Energiczny kumpel"), które klient wybiera w
aplikacji. Każdy preset to: prompt systemowy, parametry głosu, styl, granice
tematyczne i ustawienia wieku. Maskotka **rozwija się** dalej w oparciu o pamięć
długoterminową konkretnego egzemplarza (zapamiętuje imię, preferencje, wątki).
Szczegóły i format: [`docs/06-aplikacja-mobilna.md`](docs/06-aplikacja-mobilna.md)
oraz [`backend/presets/`](backend/presets).

## Struktura repozytorium

| Ścieżka | Zawartość |
|---|---|
| [`docs/01-architektura.md`](docs/01-architektura.md) | Architektura, przepływy, decyzje, warianty, koszty |
| [`docs/02-lista-czesci-BOM.md`](docs/02-lista-czesci-BOM.md) | Lista części (Pi Zero 2 W i CM4), ceny, koszt produkcji |
| [`docs/03-schemat-polaczen.md`](docs/03-schemat-polaczen.md) | Schemat połączeń, GPIO, zasilanie, ASCII-schemat |
| [`docs/04-montaz-i-uruchomienie.md`](docs/04-montaz-i-uruchomienie.md) | Montaż, obraz systemu, uruchomienie backendu |
| [`docs/05-zgodnosc-CE-EN71.md`](docs/05-zgodnosc-CE-EN71.md) | **Zgodność: CE, EN 71, RED, EMC, LVD, RoHS, baterie, RODO/GPSR** |
| [`docs/06-aplikacja-mobilna.md`](docs/06-aplikacja-mobilna.md) | Specyfikacja aplikacji, kontrakt API, presety, onboarding |
| [`device/`](device/) | Agent urządzenia (Raspberry Pi, Python) + usługa systemd |
| [`backend/`](backend/) | Zarządzany backend (FastAPI): dostawcy AI, presety, pamięć, API |
| [`app/`](app/) | Szkielet aplikacji mobilnej (Expo/React Native) + kontrakt API |

## Szybki start (deweloperski)

1. **Backend**: skonfiguruj `backend/.env` (klucze) i uruchom — patrz
   [`backend/README.md`](backend/README.md).
2. **Urządzenie**: nagraj obraz na Pi, skonfiguruj `device/config.yaml`, uruchom
   agenta — patrz [`device/README.md`](device/README.md).
3. **Aplikacja**: uruchom szkielet Expo — patrz [`app/README.md`](app/README.md).
4. Sparuj urządzenie przez aplikację, wybierz charakter, rozmawiaj.

## ⚠️ Przed wprowadzeniem do sprzedaży

Urządzenie kierowane do dzieci podlega rygorystycznym przepisom. **Przeczytaj
[`docs/05-zgodnosc-CE-EN71.md`](docs/05-zgodnosc-CE-EN71.md)** — obejmuje CE,
dyrektywy zabawkowe (EN 71), radiowe (RED), EMC, niskonapięciowe (LVD), RoHS,
WEEE, bezpieczeństwo akumulatorów (IEC 62133), GPSR oraz ochronę danych (RODO) i
bezpieczeństwo treści AI dla dzieci. Repozytorium dostarcza projekt techniczny;
**certyfikacja wymaga badań w akredytowanym laboratorium i dokumentacji
technicznej** producenta.

## Licencja

MIT — patrz [`LICENSE`](LICENSE).
