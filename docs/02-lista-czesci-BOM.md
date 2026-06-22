# 02 — Lista części (BOM) i koszt produkcji

Ceny orientacyjne (detal, 2026). Przy zakupach hurtowych/seryjnych (CM4, własna
PCB) koszty jednostkowe znacząco spadają.

## A. Wariant „kompletny" — Raspberry Pi Zero 2 W (prototyp / małe serie)

| # | Część | Przykładowy model | Ilość | Cena szt. (USD) | Uwagi |
|---|---|---|---|---|---|
| 1 | Komputer | **Raspberry Pi Zero 2 W** | 1 | 15 | WiFi+BT, Linux, sercem urządzenia |
| 2 | Karta microSD | 16–32 GB klasa A1 | 1 | 4 | System + agent |
| 3 | Mikrofon I2S | **INMP441** (MEMS) | 1 | 2 | Cyfrowy, czysty sygnał |
| 4 | Wzmacniacz I2S | **MAX98357A** | 1 | 2 | I2S→głośnik, klasa D, 3 W |
| 5 | Głośnik | 4 Ω 3 W, ~40 mm | 1 | 2 | Mały, do głowy maskotki |
| 6 | Serwo (buzia) | **SG90** micro 9 g | 1 | 1.5 | Ruch ust w rytm mowy |
| 7 | Akumulator | LiPo 1S 3.7 V 2000 mAh | 1 | 6 | Z zabezpieczeniem (PCM) |
| 8 | Ładowanie + zasilanie | **moduł 5 V boost + ładowarka 1S** (np. zintegrowany typu „power bank module") | 1 | 4 | USB-C, ochrona over/under-voltage |
| 9 | Przycisk | Taktowy / dotykowy | 1 | 0.3 | Push-to-talk / włącznik |
| 10 | LED stanu | WS2812 (1 px) lub zwykła RGB | 1 | 0.3 | Sygnalizacja stanu |
| 11 | Drobnica | Przewody, rezystory, kondensatory, mikrowłącznik | — | 2 | Filtr zasilania, podciągnięcia |
| 12 | Obudowa/mocowania | Pluszak + druk 3D na elektronikę | 1 | 3 | Mechanika ruchu buzi |
| | | | | **~52 USD** | przy detalu, 1 szt. |

> Koszt elektroniki bez pluszaka/obudowy: **~37 USD** detalicznie (1 szt.).
> Przy serii i zakupie hurtem realnie **~22–30 USD**.

### Mikrofon — alternatywy

- **USB mikrofon/karta** (np. tani USB sound card + elektret) — prostsze
  sterowniki na Pi, ale więcej miejsca i poboru. INMP441 (I2S) jest mniejszy i
  „czystszy".
- Macierz 2 mikrofonów (ReSpeaker 2-Mic HAT) — lepsze tłumienie szumu i wake-word,
  ale droższe (~10 USD) i większe.

## B. Wariant produkcyjny / skala — Raspberry Pi CM4 + własna płyta nośna

Przy większych nakładach moduł obliczeniowy CM4 + własna PCB upraszcza
certyfikację i montaż (jedna płytka: zasilanie + audio + złącza).

| # | Część | Przykład | Ilość | Cena szt. (USD) | Uwagi |
|---|---|---|---|---|---|
| 1 | Moduł obliczeniowy | **Raspberry Pi CM4** (Lite, WiFi) | 1 | 25–35 | Długa dostępność, RAM/eMMC do wyboru |
| 2 | Płyta nośna (custom PCB) | Projekt własny | 1 | 6–12 (przy serii) | Zasilanie, audio I2S, ładowarka, złącza |
| 3 | Codec/wzmacniacz audio | MAX98357A / TAS… | 1–2 | 2–4 | Zintegrowane na PCB |
| 4 | Mikrofon(y) MEMS | INMP441 / ICS-43434 | 1–2 | 2–4 | Na PCB |
| 5 | PMIC + ładowarka 1S | np. BQ25895 + boost | 1 | 3–5 | Zintegrowane zarządzanie energią |
| 6 | Akumulator | LiPo 1S 2000–3000 mAh | 1 | 6–9 | Certyfikowane ogniwo (IEC 62133) |
| 7 | Serwo + głośnik + LED + przycisk | jw. | — | ~5 | jw. |
| | | | | **~50–70 USD** | przy serii spada |

> Korzyść CM4: jedna certyfikowana PCB upraszcza badania EMC/RED i montaż,
> moduł ma deklarowaną długoterminową dostępność (ważne dla produktu rynkowego).

## C. Narzędzia (jednorazowo, dla zespołu)

- Lutownica, multimetr, czytnik kart microSD.
- Drukarka 3D (mechanika ruchu buzi, ramka elektroniki) — opcjonalnie.
- Dla wariantu CM4: zlecenie produkcji PCB (JLCPCB/PCBWay) + montaż.

## D. Uwagi do bezpieczeństwa komponentów (patrz doc 05)

- **Akumulator** musi mieć układ ochrony (PCM/BMS) i certyfikat **IEC 62133**;
  ładowanie/rozładowanie z zabezpieczeniem nad-/podnapięciowym i temperaturowym.
- **Brak małych, odłączalnych elementów** dostępnych dla dziecka (EN 71-1) —
  elektronika szczelnie zamknięta, śrubki za klapką na śrubę.
- **Materiały pluszaka** — zgodne z EN 71-2 (palność) i EN 71-3 (migracja
  pierwiastków). Wymagaj atestów od dostawcy tkanin/wypełnienia.
- **Głośność** ograniczona programowo i sprzętowo (ochrona słuchu dziecka).

## E. Szacunek kosztu produkcyjnego (orientacyjnie)

| Skala | Compute | Koszt elektroniki/szt. | Komentarz |
|---|---|---|---|
| Prototyp (1–10) | Pi Zero 2 W | ~37 USD | Detal, gotowe moduły |
| Mała seria (100–1000) | Pi Zero 2 W + montaż | ~22–30 USD | Hurt modułów |
| Produkcja (10k+) | CM4 + custom PCB | ~18–28 USD | Integracja na PCB, hurt ogniw |

Do tego: pluszak/obudowa, opakowanie, certyfikacja (jednorazowo), koszty AI
(operacyjne, pokrywane abonamentem lub kluczem klienta — patrz doc 01 §8).
