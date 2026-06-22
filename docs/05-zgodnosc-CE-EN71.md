# 05 — Zgodność i certyfikacja (CE, EN 71, RED, RODO…)

> **Disclaimer:** To opracowanie projektowe, nie porada prawna. Wprowadzenie
> zabawki z elektroniką i radiem na rynek UE wymaga **badań w akredytowanym
> laboratorium** oraz pełnej **dokumentacji technicznej** producenta. Poniżej
> mapa wymagań i checklista projektowa, aby produkt był „certyfikowalny".

## 1. Oznakowanie CE — które dyrektywy dotyczą produktu

Maskotka to **zabawka elektroniczna z modułem radiowym i akumulatorem**, więc
łączy kilka reżimów. Producent wystawia jedną **Deklarację Zgodności UE** obejmującą
wszystkie mające zastosowanie akty:

| Obszar | Akt prawny UE | Normy zharmonizowane (przykłady) |
|---|---|---|
| Bezpieczeństwo zabawek | **Dyrektywa zabawkowa 2009/48/WE** | seria **EN 71** (patrz §2) |
| Urządzenia radiowe (WiFi/BT) | **RED 2014/53/UE** | EN 300 328 (2.4 GHz), EN 301 489-x (EMC radiowe), EN 62311/62479 (ekspozycja pól EM) |
| Kompatybilność elektromag. | (objęta RED dla urządzeń radiowych) | EN 55032, EN 55035 |
| Bezpieczeństwo elektryczne / zasilacz | **LVD 2014/35/UE** (zasilacz/ładowarka) | EN 62368-1 |
| Substancje niebezpieczne | **RoHS 2011/65/UE** | EN IEC 63000 |
| Chemia w zabawkach | (w ramach EN 71-3) | EN 71-3 |
| Zużyty sprzęt / baterie | **WEEE 2012/19/UE**, **Rozp. bateryjne (UE) 2023/1542** | oznakowania, rejestracja, zbiórka |
| Ogólne bezpieczeństwo produktów | **GPSR (UE) 2023/988** | analiza ryzyka, identyfikowalność, instrukcje |
| Dane osobowe / prywatność | **RODO 2016/679** | + wytyczne dot. dzieci (patrz §6) |
| (rynek poza UE) | np. FCC/IC (USA/Kanada), UKCA (UK), CCC (Chiny) | wg rynku docelowego |

> **Połączone zabawki ("connected toys")** są pod szczególnym nadzorem (np. afera
> „My Friend Cayla"). Mikrofon + chmura + dzieci = wysoka wrażliwość prywatności.

## 2. Seria EN 71 — bezpieczeństwo zabawek (kluczowe)

| Norma | Zakres | Co znaczy dla nas |
|---|---|---|
| **EN 71-1** | Właściwości mechaniczne i fizyczne | Brak małych części odłączalnych (test cylindra dla <3 lat), brak ostrych krawędzi, wytrzymałość na upadek/zgniecenie, długość sznurków/pętli, dostęp do akumulatora tylko po odkręceniu śruby. |
| **EN 71-2** | Palność | Materiały pluszaka i wypełnienia muszą spełniać limity rozprzestrzeniania ognia. |
| **EN 71-3** | Migracja pierwiastków | Limity migracji metali ciężkich (ołów, kadm itd.) z materiałów i powłok. |
| **EN 71-9/-10/-11** | Związki organiczne | Dla niektórych materiałów/farb. |
| **EN IEC 62115** | Zabawki elektryczne — bezpieczeństwo | Nagrzewanie, izolacja, ładowanie, zwarcia, bateria. **Podstawowa dla nas.** |

### Checklista projektowa EN 71 / 62115

- [ ] Komora elektroniki i akumulatora **zamykana na śrubę** (niedostępna bez narzędzia).
- [ ] **Brak małych, odłączalnych elementów** w zasięgu dziecka (oczka, guziki = bezpieczne mocowanie).
- [ ] Temperatura obudowy w normie podczas pracy i ładowania.
- [ ] Ograniczenie **maksymalnej głośności** (ochrona słuchu) — sprzętowo + programowo.
- [ ] Materiały tekstylne z atestami EN 71-2/-3 (wymagaj od dostawcy).
- [ ] Brak ryzyka zadławienia/uduszenia (sznurki, opakowanie).
- [ ] Test wytrzymałości (upadek, ciągnięcie, gryzienie) wg metodyki EN 71-1.

## 3. RED 2014/53/UE — moduł radiowy (WiFi/BT)

Najprostsza ścieżka: użyć **modułu radiowego z istniejącą certyfikacją** (np.
Raspberry Pi Zero 2 W / CM4 mają moduły z certyfikatami), co ogranicza zakres
własnych badań. I tak konieczne:

- [ ] Badania EMC radiowe (EN 301 489-x) i widmo (EN 300 328) dla **całego wyrobu**.
- [ ] Ocena ekspozycji na pola EM (EN 62311) — istotne, bo zabawka blisko ciała.
- [ ] Antena i layout RF zgodne z dokumentacją modułu (przy CM4 + własna PCB).
- [ ] Dokumentacja: opis radia, częstotliwości, moc, instrukcja użytkownika.

## 4. Bezpieczeństwo akumulatora i ładowania

- [ ] Ogniwo **LiPo z certyfikatem IEC 62133** + układ ochrony (PCM/BMS).
- [ ] Ochrona: przeładowanie, nadmierne rozładowanie, zwarcie, nadprąd, **temperatura**.
- [ ] Ładowarka/zasilacz zgodny z **EN 62368-1** (LVD), USB-C wg specyfikacji.
- [ ] Akumulator niewymienny przez użytkownika lub w komorze na śrubę.
- [ ] Oznakowania i transport wg przepisów (UN 38.3 dla transportu ogniw).
- [ ] Rozp. bateryjne (UE) 2023/1542 — informacje, oznakowanie przekreślonego kosza.

## 5. EMC i projektowanie PCB (wariant CM4)

- [ ] Ciągła płaszczyzna masy, krótkie pętle zasilania, filtry/dławiki na liniach.
- [ ] Separacja sekcji RF; ekran nad sekcją radiową jeśli potrzeba.
- [ ] Filtrowanie I2S/PWM (serwo) by nie emitować zakłóceń.
- [ ] Testy emisji i odporności (EN 55032 / EN 55035).

## 6. RODO i ochrona dzieci (krytyczne dla „connected toy")

Mikrofon nasłuchujący w pokoju dziecka to maksymalnie wrażliwe dane. Wymagane:

- [ ] **Privacy by design/by default** — minimalizacja danych, krótka retencja audio.
- [ ] **Zgoda rodzica/opiekuna** (weryfikowalna) na przetwarzanie danych dziecka.
- [ ] Jasna informacja, **kiedy urządzenie nasłuchuje** (dioda/sygnał, push-to-talk
      domyślnie zamiast ciągłego nasłuchu).
- [ ] Możliwość **wglądu, eksportu i usunięcia** danych (prawa podmiotu danych).
- [ ] Przetwarzanie u dostawców AI: umowy powierzenia (DPA), lokalizacja danych,
      wyłączenie treningu na danych klienta tam, gdzie to możliwe.
- [ ] **Moderacja treści** dla dzieci (wej./wyj.), filtr tematów wg wieku presetu.
- [ ] Kontrola rodzicielska: limity czasu, blokady, podgląd/transkrypty, „tryb cichy".
- [ ] Bezpieczeństwo transmisji (TLS/WSS, pinning), uwierzytelnianie urządzeń,
      szyfrowanie danych w spoczynku, rotacja kluczy.
- [ ] Zgodność z wytycznymi dot. usług dla dzieci (np. UK Age Appropriate Design
      Code) na rynkach docelowych; w USA dodatkowo **COPPA**.

> Funkcje z tej listy są **wbudowane** w architekturę: push-to-talk + dioda stanu,
> moderacja w backendzie, kontrola rodzicielska w aplikacji, retencja konfigurowalna.

## 7. GPSR i dokumentacja produktu

- [ ] **Analiza ryzyka** całego wyrobu (mechanika, elektryka, radio, dane, treść AI).
- [ ] **Dokumentacja techniczna** (schematy, BOM, raporty z badań, oceny zgodności).
- [ ] **Deklaracja Zgodności UE** podpisana przez producenta.
- [ ] Oznakowania na wyrobie/opakowaniu: **CE**, dane producenta/importera, model,
      przekreślony kosz (WEEE/baterie), ostrzeżenia wiekowe (np. „nieodpowiednie
      dla dzieci poniżej 3 lat" jeśli dotyczy), piktogramy.
- [ ] **Instrukcja** w językach rynków docelowych + ostrzeżenia bezpieczeństwa.
- [ ] Identyfikowalność (nr serii/partii), kontakt do zgłoszeń.

## 8. Proces dojścia do CE (skrót)

1. Zaprojektuj wg powyższych checklist (ten projekt to ułatwia).
2. Wybierz **akredytowane laboratorium** (TÜV, SGS, Bureau Veritas, Intertek itp.).
3. Zleć badania: EN 71 (-1/-2/-3, 62115), RED (300 328, 301 489, 62311), EMC,
   LVD/zasilacz, RoHS, bateria.
4. Uzupełnij ocenę ryzyka, prywatności (DPIA dla danych dzieci) i dokumentację.
5. Wystaw Deklarację Zgodności UE, nanieś oznakowania, zarejestruj WEEE/baterie.
6. Monitoruj rynek (obowiązki posprzedażowe, zgłaszanie incydentów).

## 9. Tani sposób na ograniczenie zakresu badań

- Użyj **pre-certyfikowanych modułów** radiowych (Pi/CM4) — mniej własnych badań RF.
- Użyj **gotowego, certyfikowanego zasilacza/ładowarki** (EN 62368-1).
- Kupuj **tkaniny/wypełnienia z atestami EN 71** od sprawdzonych dostawców.
- Zaprojektuj mechanikę „od początku pod EN 71" (brak małych części, komora na śrubę).
- Prywatność i moderacja **wbudowane** (jak w tym projekcie) — łatwiejsza ocena DPIA.
