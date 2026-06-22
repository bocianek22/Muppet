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

## Sklepy PL/UE (szybsza dostawa) i dystrybutorzy

Linki to **wyszukiwarki** sklepów. Dystrybutorzy (TME/Botland/Kamami) mają zwykle
oryginalne komponenty, faktury VAT i szybką wysyłkę w UE — wygodne do prototypu i
serii. Mouser/Digi-Key/Farnell — gdy potrzebujesz **części z certyfikatami i
kartami katalogowymi** (produkcja, audyt zgodności).

| Część | TME | Botland | Kamami |
|---|---|---|---|
| Raspberry Pi Zero 2 W | [szukaj](https://www.tme.eu/en/katalog/?search=raspberry%20pi%20zero%202%20w) | [szukaj](https://botland.store/search?s=raspberry%20pi%20zero%202%20w) | [szukaj](https://kamami.pl/szukaj?s=raspberry%20pi%20zero%202%20w) |
| microSD 32GB A1 | [szukaj](https://www.tme.eu/en/katalog/?search=microsd%2032gb) | [szukaj](https://botland.store/search?s=microsd%2032gb) | [szukaj](https://kamami.pl/szukaj?s=microsd%2032gb) |
| INMP441 (mic I2S) | [szukaj](https://www.tme.eu/en/katalog/?search=INMP441) | [szukaj](https://botland.store/search?s=INMP441) | [szukaj](https://kamami.pl/szukaj?s=INMP441) |
| MAX98357A (wzm. I2S) | [szukaj](https://www.tme.eu/en/katalog/?search=MAX98357A) | [szukaj](https://botland.store/search?s=MAX98357A) | [szukaj](https://kamami.pl/szukaj?s=MAX98357A) |
| Głośnik 4Ω 3W | [szukaj](https://www.tme.eu/en/katalog/?search=loudspeaker%204ohm%203w) | [szukaj](https://botland.store/search?s=g%C5%82o%C5%9Bnik%204ohm%203w) | [szukaj](https://kamami.pl/szukaj?s=g%C5%82o%C5%9Bnik%204%20ohm) |
| Serwo SG90 | [szukaj](https://www.tme.eu/en/katalog/?search=SG90) | [szukaj](https://botland.store/search?s=SG90) | [szukaj](https://kamami.pl/szukaj?s=SG90) |
| Akumulator LiPo 1S 2000mAh | [szukaj](https://www.tme.eu/en/katalog/?search=akumulator%20li-po%203.7v%202000mah) | [szukaj](https://botland.store/search?s=akumulator%20li-po%203.7v%202000mah) | [szukaj](https://kamami.pl/szukaj?s=li-po%203.7v%202000mah) |
| Ładowarka/boost 5V (TP4056/MT3608) | [TP4056](https://www.tme.eu/en/katalog/?search=TP4056) · [MT3608](https://www.tme.eu/en/katalog/?search=MT3608) | [TP4056](https://botland.store/search?s=TP4056) · [boost 5V](https://botland.store/search?s=przetwornica%20step-up%205v) | [TP4056](https://kamami.pl/szukaj?s=TP4056) |
| Przycisk / TTP223 | [tact](https://www.tme.eu/en/katalog/?search=tact%20switch%2012mm) · [TTP223](https://www.tme.eu/en/katalog/?search=TTP223) | [TTP223](https://botland.store/search?s=TTP223) | [TTP223](https://kamami.pl/szukaj?s=TTP223) |
| LED WS2812 | [szukaj](https://www.tme.eu/en/katalog/?search=WS2812) | [szukaj](https://botland.store/search?s=WS2812) | [szukaj](https://kamami.pl/szukaj?s=WS2812) |
| Przewody Dupont Ž-Ž | [szukaj](https://www.tme.eu/en/katalog/?search=jumper%20wires%20female) | [szukaj](https://botland.store/search?s=przewody%20%C5%BCe%C5%84sko-%C5%Bce%C5%84skie) | [szukaj](https://kamami.pl/szukaj?s=przewody%20dupont) |
| Kondensator 1000µF | [szukaj](https://www.tme.eu/en/katalog/?search=1000uf%2010v%20electrolytic) | [szukaj](https://botland.store/search?s=kondensator%201000uf) | [szukaj](https://kamami.pl/szukaj?s=kondensator%201000uf) |

> **Dystrybutorzy globalni (produkcja/certyfikacja):**
> [Mouser](https://www.mouser.com/), [Digi-Key](https://www.digikey.com/),
> [Farnell/element14](https://www.farnell.com/). Tam kupisz ogniwa LiPo z
> certyfikatem IEC 62133, układy ładowania (np. BQ25895), codeki audio i
> komponenty z pełnymi kartami katalogowymi — pod wariant CM4 i audyt zgodności
> ([`docs/05-zgodnosc-CE-EN71.md`](05-zgodnosc-CE-EN71.md)).

> Dostępność Raspberry Pi sprawdzisz globalnie na
> [rpilocator.com](https://rpilocator.com/).

## Sklepy hobbystyczne (UE / UK / US)

Wygodne, gdy chcesz gotowe moduły „pod Raspberry Pi" z jednego koszyka.

| Część | Pimoroni | The Pi Hut | Adafruit |
|---|---|---|---|
| Raspberry Pi Zero 2 W | [szukaj](https://shop.pimoroni.com/search?q=raspberry%20pi%20zero%202%20w) | [szukaj](https://thepihut.com/search?q=raspberry%20pi%20zero%202%20w) | [szukaj](https://www.adafruit.com/search?q=raspberry%20pi%20zero%202%20w) |
| Mikrofon I2S (INMP441/SPH0645) | [szukaj](https://shop.pimoroni.com/search?q=i2s%20microphone) | [szukaj](https://thepihut.com/search?q=i2s%20microphone) | [szukaj](https://www.adafruit.com/search?q=i2s%20microphone) |
| Wzmacniacz I2S MAX98357A | [szukaj](https://shop.pimoroni.com/search?q=MAX98357A) | [szukaj](https://thepihut.com/search?q=MAX98357A) | [szukaj](https://www.adafruit.com/search?q=MAX98357A) |
| Głośnik 4Ω 3W | [szukaj](https://shop.pimoroni.com/search?q=speaker%204%20ohm) | [szukaj](https://thepihut.com/search?q=speaker%204%20ohm) | [szukaj](https://www.adafruit.com/search?q=speaker%204%20ohm%203w) |
| Serwo SG90 | [szukaj](https://shop.pimoroni.com/search?q=micro%20servo) | [szukaj](https://thepihut.com/search?q=sg90%20servo) | [szukaj](https://www.adafruit.com/search?q=micro%20servo) |
| Akumulator LiPo 1S | [szukaj](https://shop.pimoroni.com/search?q=lipo%20battery) | [szukaj](https://thepihut.com/search?q=lipo%20battery) | [szukaj](https://www.adafruit.com/search?q=lithium%20ion%20polymer%20battery) |
| Ładowarka/boost (PowerBoost) | [szukaj](https://shop.pimoroni.com/search?q=powerboost) | [szukaj](https://thepihut.com/search?q=lipo%20charger%20boost) | [szukaj](https://www.adafruit.com/search?q=powerboost) |
| LED WS2812 (NeoPixel) | [szukaj](https://shop.pimoroni.com/search?q=neopixel) | [szukaj](https://thepihut.com/search?q=neopixel) | [szukaj](https://www.adafruit.com/search?q=neopixel) |

## Wariant produkcyjny CM4 — zakupy (Mouser / Digi-Key)

Pod większą skalę: **moduł CM4 + własna płyta nośna** (zasilanie, audio, ładowarka,
złącza na jednej PCB). Komponenty z certyfikatami i kartami katalogowymi bierz od
dystrybutorów globalnych; PCB zleć w JLCPCB/PCBWay. Kontekst i koszty:
[`docs/02-lista-czesci-BOM.md`](02-lista-czesci-BOM.md) §B.

| Część | Po co | Mouser | Digi-Key |
|---|---|---|---|
| Raspberry Pi CM4 (Lite, WiFi) | moduł obliczeniowy | [szukaj](https://www.mouser.com/c/?q=raspberry%20pi%20compute%20module%204) | [szukaj](https://www.digikey.com/en/products/result?keywords=raspberry%20pi%20compute%20module%204) |
| Złącza CM4 (2× Hirose DF40) | montaż CM4 na PCB | [szukaj](https://www.mouser.com/c/?q=DF40C-100DS) | [szukaj](https://www.digikey.com/en/products/result?keywords=DF40C-100DS) |
| Mikrofon MEMS I2S ICS-43434 | mikrofon na PCB | [szukaj](https://www.mouser.com/c/?q=ICS-43434) | [szukaj](https://www.digikey.com/en/products/result?keywords=ICS-43434) |
| Wzmacniacz I2S MAX98357A (IC) | audio na PCB | [szukaj](https://www.mouser.com/c/?q=MAX98357A) | [szukaj](https://www.digikey.com/en/products/result?keywords=MAX98357AETE%2BT) |
| Ładowarka 1S BQ25895 | zarządzanie energią | [szukaj](https://www.mouser.com/c/?q=BQ25895) | [szukaj](https://www.digikey.com/en/products/result?keywords=BQ25895) |
| Przetwornica step-up 5V (TPS61088) | szyna 5V | [szukaj](https://www.mouser.com/c/?q=TPS61088) | [szukaj](https://www.digikey.com/en/products/result?keywords=TPS61088) |
| Ogniwo LiPo 1S (cert. IEC 62133) | akumulator | [szukaj](https://www.mouser.com/c/?q=lithium%20polymer%20battery%20IEC%2062133) | [szukaj](https://www.digikey.com/en/products/result?keywords=lithium%20polymer%20battery) |
| Złącze USB-C (zasilanie) | ładowanie | [szukaj](https://www.mouser.com/c/?q=usb-c%20receptacle%20power) | [szukaj](https://www.digikey.com/en/products/result?keywords=usb-c%20receptacle) |
| Serwo / głośnik / WS2812 / przycisk | mechanika + UI | jak w tabeli głównej / dystrybutorzy PL | — |

> Pamiętaj o RED/EMC przy własnej PCB: użyj modułu CM4 z **certyfikowanym radiem**
> i zaprojektuj layout RF wg dokumentacji — patrz
> [`docs/05-zgodnosc-CE-EN71.md`](05-zgodnosc-CE-EN71.md) §3 i §5.
> Produkcja PCB: [JLCPCB](https://jlcpcb.com/), [PCBWay](https://www.pcbway.com/).
