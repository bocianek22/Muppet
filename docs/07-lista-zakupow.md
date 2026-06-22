# 07 — Lista zakupów (wariant prototyp: Raspberry Pi Zero 2 W)

Linki to **wyszukiwania** (stabilne — pojedyncze oferty szybko wygasają). Wybierz
ofertę z dobrymi opiniami i wysyłką do Ciebie. Ceny orientacyjne (2026, detal).

> Uwaga: Raspberry Pi **nie jest klonowane** — kupuj u autoryzowanych
> dystrybutorów (np. botland, kamami, rpilocator do znalezienia dostępności) lub
> sprawdzonych sprzedawców eBay. Pozostałe moduły mają tanie odpowiedniki na
> AliExpress/eBay.

| # | Część | Ilość | ~Cena | AliExpress | eBay |
|---|---|---|---|---|---|
| 1 | **Raspberry Pi Zero 2 W** | 1 | $15–25 | [szukaj](https://www.aliexpress.com/w/wholesale-raspberry-pi-zero-2-w.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=raspberry+pi+zero+2+w) |
| 2 | **Karta microSD 32GB A1** (SanDisk/Samsung) | 1 | $4–7 | [szukaj](https://www.aliexpress.com/w/wholesale-sandisk-microsd-32gb-a1.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=microsd+32gb+a1) |
| 3 | **Mikrofon I2S INMP441** (moduł) | 1 | $2–4 | [szukaj](https://www.aliexpress.com/w/wholesale-INMP441.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=INMP441) |
| 4 | **Wzmacniacz I2S MAX98357A** (moduł) | 1 | $2–4 | [szukaj](https://www.aliexpress.com/w/wholesale-MAX98357A.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=MAX98357A) |
| 5 | **Głośnik 4Ω 3W ~40mm** | 1 | $1–3 | [szukaj](https://www.aliexpress.com/w/wholesale-speaker-4ohm-3w-40mm.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=4ohm+3w+speaker+40mm) |
| 6 | **Serwo SG90** (micro 9g) | 1 | $1–2 | [szukaj](https://www.aliexpress.com/w/wholesale-SG90-servo.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=sg90+servo) |
| 7 | **Akumulator LiPo 1S 3.7V 2000mAh** (z PCM, JST) | 1 | $5–8 | [szukaj](https://www.aliexpress.com/w/wholesale-lipo-3.7v-2000mah-jst.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=lipo+3.7v+2000mah+protected) |
| 8 | **Moduł ładowarka 1S + boost 5V** (np. typu power-bank / „134N3P") | 1 | $2–4 | [szukaj](https://www.aliexpress.com/w/wholesale-5v-boost-charger-module-power-bank.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=5v+boost+charger+module+power+bank) |
| 8b | *(alternatywa)* TP4056 (ładowanie) + MT3608 (boost 5V) | 1+1 | $1–2 | [TP4056](https://www.aliexpress.com/w/wholesale-TP4056.html) / [MT3608](https://www.aliexpress.com/w/wholesale-MT3608.html) | [TP4056](https://www.ebay.com/sch/i.html?_nkw=tp4056) |
| 9 | **Przycisk** taktowy 12mm *lub* dotykowy TTP223 | 1 | $0.3–1 | [taktowy](https://www.aliexpress.com/w/wholesale-tactile-button-12mm.html) / [TTP223](https://www.aliexpress.com/w/wholesale-TTP223.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=ttp223+touch) |
| 10 | **LED WS2812** (moduł 1 piksel) | 1 | $0.3–1 | [szukaj](https://www.aliexpress.com/w/wholesale-ws2812-module.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=ws2812+module) |
| 11 | **Przewody Dupont (Ž-Ž)** | 1 zest. | $1–3 | [szukaj](https://www.aliexpress.com/w/wholesale-dupont-wires-female-female.html) | [szukaj](https://www.ebay.com/sch/i.html?_nkw=dupont+wires+female) |
| 12 | **Kondensator elektrolit. 1000µF/6.3–10V** (dla serwa) | 1–2 | $0.5 | [szukaj](https://www.aliexpress.com/w/wholesale-1000uf-electrolytic-capacitor.html) | — |
| 13 | **Goldpiny / listwa do lutowania Pi Zero** (jeśli bez wlutowanych) | 1 | $0.5–1 | [szukaj](https://www.aliexpress.com/w/wholesale-raspberry-pi-zero-header.html) | — |

**Razem elektronika:** ~**$35–55** detalicznie (1 szt.); przy zakupie kilku
sztuk/hurtem realnie taniej.

## Wskazówki przy wyborze ofert

- **Pi Zero 2 W** — bywa trudno dostępne; jeśli brak, sprawdź autoryzowanych
  dystrybutorów. Wersja **WH** ma już wlutowane goldpiny (poz. 13 zbędna).
- **Akumulator** — koniecznie z układem ochrony (PCM/BMS). Do produktu rynkowego
  wymagaj ogniwa z certyfikatem **IEC 62133** (patrz
  [`docs/05-zgodnosc-CE-EN71.md`](05-zgodnosc-CE-EN71.md)).
- **Moduł zasilania (poz. 8)** — wygodny jest gotowy moduł „power-bank" z USB-C,
  ładowaniem 1S, boostem 5V i ochroną w jednym. Wariant 8b (TP4056+MT3608) jest
  tańszy, ale wymaga więcej połączeń.
- **Mikrofon** — INMP441 (I2S) jest mały i „czysty". Dla lepszego tłumienia szumu
  i wake-word rozważ ReSpeaker 2-Mic (droższy):
  [szukaj](https://www.aliexpress.com/w/wholesale-respeaker-2-mic.html).
- **Lutownica** potrzebna do goldpinów Pi i ewentualnie modułów audio.

## Co dalej (wariant produkcyjny CM4)

Przy serii przechodzi się na **Raspberry Pi CM4 + własną płytę nośną** (zasilanie,
audio, ładowarka, złącza na jednej PCB). Szczegóły i koszty:
[`docs/02-lista-czesci-BOM.md`](02-lista-czesci-BOM.md) §B.
