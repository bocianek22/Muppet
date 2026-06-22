// Klient REST backendu Muppet AI. Kontrakt: docs/06-aplikacja-mobilna.md

import { API_BASE_URL } from "./config";

export type Preset = {
  id: string;
  name: string;
  description: string;
  age_range: string;
  language: string;
  provider_profile?: string;
};

export type Profile = {
  preset_id: string;
  style: Record<string, number>;
  language: string;
  extra_instructions: string;
  provider_profile: string;
  voice: Record<string, unknown>;
  parental: Record<string, unknown>;
};

function authHeaders(token: string): Record<string, string> {
  return { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
}

export async function fetchPresets(language?: string): Promise<Preset[]> {
  const q = language ? `?language=${encodeURIComponent(language)}` : "";
  const res = await fetch(`${API_BASE_URL}/presets${q}`);
  if (!res.ok) throw new Error(`Błąd presetów: ${res.status}`);
  return res.json();
}

export async function getProfile(deviceId: string, token: string): Promise<Profile> {
  const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/profile`, {
    headers: authHeaders(token),
  });
  if (!res.ok) throw new Error(`Błąd profilu: ${res.status}`);
  return res.json();
}

export async function updateProfile(
  deviceId: string,
  token: string,
  patch: Partial<Profile>
): Promise<Profile> {
  const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/profile`, {
    method: "PUT",
    headers: authHeaders(token),
    body: JSON.stringify(patch),
  });
  if (!res.ok) throw new Error(`Błąd zapisu profilu: ${res.status}`);
  return res.json();
}

export async function getMemory(deviceId: string, token: string): Promise<unknown> {
  const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/memory`, {
    headers: authHeaders(token),
  });
  if (!res.ok) throw new Error(`Błąd pamięci: ${res.status}`);
  return res.json();
}

export async function clearMemory(deviceId: string, token: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/devices/${deviceId}/memory`, {
    method: "DELETE",
    headers: authHeaders(token),
  });
  if (!res.ok) throw new Error(`Błąd czyszczenia pamięci: ${res.status}`);
}

export async function enrollDevice(
  enrollToken: string,
  deviceId: string
): Promise<{ device_id: string; device_token: string }> {
  const res = await fetch(`${API_BASE_URL}/devices/enroll`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enroll_token: enrollToken, device_id: deviceId }),
  });
  if (!res.ok) throw new Error(`Błąd parowania: ${res.status}`);
  return res.json();
}
