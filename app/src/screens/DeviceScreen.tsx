import React, { useEffect, useState } from "react";
import { Button, ScrollView, StyleSheet, Switch, Text, View } from "react-native";

import { clearMemory, getMemory, getProfile, updateProfile, Profile } from "../api";
import { DEV_DEVICE_ID, DEV_DEVICE_TOKEN } from "../config";

export default function DeviceScreen() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [memory, setMemory] = useState<string>("");
  const [premium, setPremium] = useState(true);

  async function refresh() {
    const p = await getProfile(DEV_DEVICE_ID, DEV_DEVICE_TOKEN);
    setProfile(p);
    setPremium(p.provider_profile === "premium");
    setMemory(JSON.stringify(await getMemory(DEV_DEVICE_ID, DEV_DEVICE_TOKEN), null, 2));
  }

  useEffect(() => {
    refresh().catch(() => {});
  }, []);

  async function togglePremium(value: boolean) {
    setPremium(value);
    await updateProfile(DEV_DEVICE_ID, DEV_DEVICE_TOKEN, {
      provider_profile: value ? "premium" : "base",
    });
  }

  async function onClearMemory() {
    await clearMemory(DEV_DEVICE_ID, DEV_DEVICE_TOKEN);
    await refresh();
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Urządzenie</Text>
      <Text style={styles.label}>Aktywny charakter: {profile?.preset_id ?? "—"}</Text>
      <Text style={styles.label}>Język: {profile?.language ?? "—"}</Text>

      <View style={styles.row}>
        <Text style={styles.label}>Tryb premium (Claude + ElevenLabs)</Text>
        <Switch value={premium} onValueChange={togglePremium} />
      </View>

      <Text style={[styles.title, { marginTop: 20 }]}>Pamięć maskotki</Text>
      <Text style={styles.mono}>{memory || "(pusta)"}</Text>
      <Button title="Wyczyść pamięć (RODO)" color="#c00" onPress={onClearMemory} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 20, fontWeight: "600", marginBottom: 10 },
  label: { fontSize: 15, marginBottom: 8 },
  row: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginVertical: 8 },
  mono: { fontFamily: "monospace", backgroundColor: "#f2f2f7", padding: 10, borderRadius: 8, marginBottom: 12 },
});
