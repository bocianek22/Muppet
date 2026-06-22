import React, { useEffect, useState } from "react";
import { ActivityIndicator, FlatList, StyleSheet, Text, TouchableOpacity, View } from "react-native";

import { fetchPresets, updateProfile, Preset } from "../api";
import { DEV_DEVICE_ID, DEV_DEVICE_TOKEN } from "../config";

export default function PresetsScreen() {
  const [presets, setPresets] = useState<Preset[]>([]);
  const [loading, setLoading] = useState(true);
  const [active, setActive] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPresets("pl")
      .then(setPresets)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  async function choose(preset: Preset) {
    try {
      await updateProfile(DEV_DEVICE_ID, DEV_DEVICE_TOKEN, { preset_id: preset.id });
      setActive(preset.id);
    } catch (e) {
      setError(String(e));
    }
  }

  if (loading) return <ActivityIndicator style={{ marginTop: 40 }} />;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Wybierz charakter maskotki</Text>
      {error && <Text style={styles.error}>{error}</Text>}
      <FlatList
        data={presets}
        keyExtractor={(p) => p.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.card, active === item.id && styles.cardActive]}
            onPress={() => choose(item)}
          >
            <Text style={styles.name}>{item.name}</Text>
            <Text style={styles.desc}>{item.description}</Text>
            <Text style={styles.meta}>Wiek: {item.age_range}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 20, fontWeight: "600", marginBottom: 12 },
  card: { padding: 14, borderRadius: 12, backgroundColor: "#f2f2f7", marginBottom: 10 },
  cardActive: { backgroundColor: "#d9efff", borderColor: "#0a84ff", borderWidth: 2 },
  name: { fontSize: 16, fontWeight: "600" },
  desc: { color: "#444", marginTop: 4 },
  meta: { color: "#888", marginTop: 6, fontSize: 12 },
  error: { color: "#c00", marginBottom: 8 },
});
