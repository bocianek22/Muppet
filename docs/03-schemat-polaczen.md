# 03 — Schemat połączeń (Raspberry Pi Zero 2 W)

Połączenia dla wariantu prototypowego z gotowymi modułami. Numeracja pinów wg
**BCM** (GPIO) oraz fizyczna (pin na 40-pinowym złączu Pi).

## 1. Tabela połączeń

### Mikrofon I2S — INMP441 (wejście, I2S RX)

| INMP441 | Pi (BCM / pin fiz.) | Opis |
|---|---|---|
| VDD | 3V3 (pin 1) | Zasilanie 3.3 V |
| GND | GND (pin 6) | Masa |
| SD  | GPIO20 / pin 38 | I2S DIN (dane z mikrofonu) |
| WS  | GPIO19 / pin 35 | I2S LRCLK (word select) |
| SCK | GPIO18 / pin 12 | I2S BCLK (bit clock) |
| L/R | GND | Kanał lewy (mono) |

### Wzmacniacz I2S — MAX98357A (wyjście, I2S TX)

| MAX98357A | Pi (BCM / pin fiz.) | Opis |
|---|---|---|
| VIN | 5V (pin 2) | Zasilanie 5 V |
| GND | GND (pin 9) | Masa |
| DIN | GPIO21 / pin 40 | I2S DOUT (dane do głośnika) |
| LRC | GPIO19 / pin 35 | I2S LRCLK (współdzielony z mikrofonem) |
| BCLK| GPIO18 / pin 12 | I2S BCLK (współdzielony) |
| GAIN| (zob. niżej) | Ustawienie wzmocnienia |
| SD  | 3V3 lub GPIO | Shutdown / wybór kanału |
| +/- | Głośnik 4 Ω | Wyjście na głośnik |

> Pi ma jedną szynę I2S — BCLK (GPIO18) i LRCLK (GPIO19) są **współdzielone**
> między mikrofonem a wzmacniaczem; różnią się tylko linie danych (DIN/DOUT).

### Serwo ruchu buzi — SG90

| SG90 | Połączenie | Opis |
|---|---|---|
| VCC (czerw.) | 5 V (z modułu zasilania, **nie** z 3V3 Pi) | Serwo pobiera prąd impulsowo |
| GND (brąz.)  | GND wspólna | Masa wspólna z Pi |
| Sygnał (pom.)| GPIO12 / pin 32 (PWM) | Sterowanie PWM (50 Hz) |

> Serwo zasilaj z szyny 5 V modułu zasilania, masę połącz z Pi. Dodaj
> kondensator elektrolityczny (np. 470–1000 µF) blisko serwa, by tłumić skoki.

### Przycisk (push-to-talk / włącznik)

| Przycisk | Pi | Opis |
|---|---|---|
| Pin 1 | GPIO16 / pin 36 | Wejście z podciągnięciem (pull-up wewn.) |
| Pin 2 | GND | Zwarcie do masy przy wciśnięciu |

### LED stanu — WS2812 (1 piksel) lub zwykła LED

| WS2812 | Pi | Opis |
|---|---|---|
| VDD | 5 V | Zasilanie |
| GND | GND | Masa |
| DIN | GPIO13 / pin 33 | Dane (sygnalizacja stanu) |

### Zasilanie

```
[Akumulator LiPo 1S 3.7V] ──► [Moduł: ładowarka 1S + boost 5V + ochrona] ──► 5V/GND
                                          ▲ USB-C (ładowanie)
   5V/GND zasila:  Raspberry Pi (5V pin 2/4, GND), MAX98357A (VIN), serwo (VCC)
   3V3 (z Pi) zasila: INMP441 (VDD)
```

## 2. ASCII-schemat poglądowy

```
                         +-------------------- Raspberry Pi Zero 2 W (BCM) ------+
                         |                                                       |
  INMP441 (mic)          |  GPIO18 (BCLK) ──┬───────────────► MAX98357A BCLK     |
   VDD ── 3V3 ───────────┤  GPIO19 (LRCLK) ─┼──┬────────────► MAX98357A LRC      |
   GND ── GND ───────────┤                  │  │                                 |
   SCK ── GPIO18 ────────┘                  │  │                                 |
   WS  ── GPIO19 ───────────────────────────┘  │                                 |
   SD  ── GPIO20 (I2S DIN) ─────────────────────┘                                 |
   L/R ── GND                                                                     |
                         |  GPIO21 (I2S DOUT) ────────────► MAX98357A DIN         |
                         |                                   MAX98357A +/- ─► [Głośnik 4Ω]
                         |  GPIO12 (PWM) ─────────────────► SG90 sygnał          |
                         |  GPIO16 ◄────[Przycisk]──── GND                        |
                         |  GPIO13 ─────────────────────► WS2812 DIN             |
                         |  5V / GND  ◄── moduł zasilania ◄── [LiPo 1S]          |
                         +-------------------------------------------------------+
```

## 3. Konfiguracja I2S w systemie (Raspberry Pi OS)

W `/boot/firmware/config.txt` (lub `/boot/config.txt`) włącz I2S i nakładki:

```ini
dtparam=i2s=on
dtparam=audio=off            # wyłącz wbudowane audio (jack), używamy I2S
# Wyjście I2S (MAX98357A):
dtoverlay=max98357a,sdmode-pin=4
# Wejście I2S (INMP441) jako urządzenie capture:
dtoverlay=googlevoicehat-soundcard   # częsty, kompatybilny overlay dla I2S mic
```

> Konkretne overlaye zależą od dystrybucji/jądra. Alternatywnie użyj overlaya
> `i2s-mmap` + `simple-audio-card` lub gotowego HAT-a. Szczegóły kroków w
> [`docs/04-montaz-i-uruchomienie.md`](04-montaz-i-uruchomienie.md).

## 4. Wersja produkcyjna (CM4) — uwagi do PCB

Przy wariancie CM4 powyższe moduły integrujemy na jednej płycie nośnej:

- Sekcja zasilania: ładowarka 1S (np. BQ25895) + boost 5 V + ochrona ogniwa,
  pomiar napięcia/temperatury akumulatora.
- Audio: codec/wzmacniacz I2S + mikrofon(y) MEMS na PCB, filtry EMI.
- Złącza: serwo, głośnik, przycisk, LED, USB-C, antena WiFi/BT (lub moduł CM4 z
  anteną zewn. + cert. RED).
- Rozplanowanie pod **EMC/RED**: masa ciągła, dławiki na liniach zasilania,
  ekranowanie sekcji RF — patrz [`docs/05-zgodnosc-CE-EN71.md`](05-zgodnosc-CE-EN71.md).
