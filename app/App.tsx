import React, { useState } from "react";
import { SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { StatusBar } from "expo-status-bar";

import PresetsScreen from "./src/screens/PresetsScreen";
import DeviceScreen from "./src/screens/DeviceScreen";
import PairScreen from "./src/screens/PairScreen";

type Tab = "pair" | "presets" | "device";

// Minimalna nawigacja zakładkami (bez dodatkowych zależności).
// W produkcji warto użyć react-navigation.
export default function App() {
  const [tab, setTab] = useState<Tab>("presets");

  return (
    <SafeAreaView style={styles.root}>
      <StatusBar style="dark" />
      <View style={styles.screen}>
        {tab === "pair" && <PairScreen />}
        {tab === "presets" && <PresetsScreen />}
        {tab === "device" && <DeviceScreen />}
      </View>
      <View style={styles.tabbar}>
        <TabButton label="Parowanie" active={tab === "pair"} onPress={() => setTab("pair")} />
        <TabButton label="Charaktery" active={tab === "presets"} onPress={() => setTab("presets")} />
        <TabButton label="Urządzenie" active={tab === "device"} onPress={() => setTab("device")} />
      </View>
    </SafeAreaView>
  );
}

function TabButton({ label, active, onPress }: { label: string; active: boolean; onPress: () => void }) {
  return (
    <TouchableOpacity style={styles.tab} onPress={onPress}>
      <Text style={[styles.tabText, active && styles.tabActive]}>{label}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: "#fff" },
  screen: { flex: 1 },
  tabbar: { flexDirection: "row", borderTopWidth: 1, borderTopColor: "#eee" },
  tab: { flex: 1, paddingVertical: 12, alignItems: "center" },
  tabText: { color: "#888", fontSize: 14 },
  tabActive: { color: "#0a84ff", fontWeight: "700" },
});
