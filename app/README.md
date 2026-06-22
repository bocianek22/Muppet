# Aplikacja mobilna Muppet AI (szkielet Expo / React Native)

Startowy szkielet aplikacji klienta: parowanie urządzenia (BLE), wybór charakteru
(preset), dostrajanie i kontrola rodzicielska. Pełna specyfikacja i kontrakt API:
[`docs/06-aplikacja-mobilna.md`](../docs/06-aplikacja-mobilna.md).

## Uruchomienie

```bash
npm install
npx expo start
```

Ustaw adres backendu w `src/config.ts` (`API_BASE_URL`).

## Zawartość szkieletu

| Plik | Rola |
|---|---|
| `App.tsx` | Prosta nawigacja między ekranami |
| `src/config.ts` | Adres API i stałe |
| `src/api.ts` | Klient REST backendu (presety, profil, pamięć) |
| `src/ble.ts` | Provisioning WiFi przez BLE (szkielet/kontrakt) |
| `src/screens/PresetsScreen.tsx` | Galeria charakterów i wybór |
| `src/screens/DeviceScreen.tsx` | Profil urządzenia, styl, pamięć |
| `src/screens/PairScreen.tsx` | Parowanie urządzenia (BLE → WiFi) |

## Co dodać do produkcji

- Konto i autoryzacja (JWT/OAuth), zgody RODO (zgoda rodzica).
- `react-native-ble-plx` do realnej komunikacji BLE (tu jest szkielet/kontrakt).
- Kontrola rodzicielska (limity czasu, blokady tematów, godziny ciszy).
- Historia/transkrypty, tryb „własny klucz API" (BYOK), zarządzanie planem.
- Obsługa wielu urządzeń, powiadomienia, lokalizacja (i18n).
