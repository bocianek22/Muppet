// Szkielet provisioningu WiFi przez BLE.
//
// W produkcji użyj `react-native-ble-plx`. Tu opisujemy KONTRAKT GATT i podajemy
// zaślepki, aby reszta aplikacji się kompilowała i miała stabilne API.
//
// Usługa konfiguracyjna urządzenia (w trybie parowania) — charakterystyki:
//   wifi_ssid    (write)
//   wifi_pass    (write, szyfrowane)
//   enroll_token (write)  — token z konta klienta
//   status       (notify) — provisioning|connecting|online|error:<kod>

export type ProvisioningStatus =
  | "scanning"
  | "connecting"
  | "writing"
  | "online"
  | "error";

export type ProvisioningResult = {
  status: ProvisioningStatus;
  deviceId?: string;
  message?: string;
};

export async function scanForMuppet(): Promise<string[]> {
  // TODO: BleManager.startDeviceScan(...) → zwróć listę identyfikatorów maskotek.
  return ["Muppet-XXYY (demo)"];
}

export async function provisionWifi(params: {
  deviceBleId: string;
  ssid: string;
  password: string;
  enrollToken: string;
  onStatus?: (s: ProvisioningStatus) => void;
}): Promise<ProvisioningResult> {
  const { onStatus } = params;
  // TODO (react-native-ble-plx):
  //  1) connect(deviceBleId)
  //  2) write wifi_ssid, wifi_pass, enroll_token
  //  3) subscribe status (notify) aż "online" lub "error:<kod>"
  onStatus?.("connecting");
  onStatus?.("writing");
  onStatus?.("online");
  return { status: "online", deviceId: "dev_demo" };
}
