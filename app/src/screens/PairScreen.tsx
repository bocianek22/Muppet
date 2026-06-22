import React, { useState } from "react";
import { Button, StyleSheet, Text, TextInput, View } from "react-native";

import { provisionWifi, ProvisioningStatus } from "../ble";

export default function PairScreen() {
  const [ssid, setSsid] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<ProvisioningStatus | "">("");

  async function pair() {
    setStatus("connecting");
    const res = await provisionWifi({
      deviceBleId: "demo",
      ssid,
      password,
      enrollToken: "enroll-demo",
      onStatus: setStatus,
    });
    setStatus(res.status);
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Parowanie maskotki</Text>
      <Text style={styles.help}>
        Włącz maskotkę (dioda miga = tryb parowania) i podaj dane sieci WiFi.
      </Text>
      <TextInput style={styles.input} placeholder="Nazwa sieci WiFi (SSID)" value={ssid} onChangeText={setSsid} />
      <TextInput
        style={styles.input}
        placeholder="Hasło WiFi"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Sparuj przez Bluetooth" onPress={pair} />
      {status ? <Text style={styles.status}>Status: {status}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, justifyContent: "center" },
  title: { fontSize: 22, fontWeight: "700", marginBottom: 8 },
  help: { color: "#555", marginBottom: 16 },
  input: { borderWidth: 1, borderColor: "#ccc", borderRadius: 8, padding: 12, marginBottom: 12 },
  status: { marginTop: 16, fontSize: 15 },
});
