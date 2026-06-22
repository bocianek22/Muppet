"""Profil urządzenia: aktywny preset + dostrojenia + ustawienia rodzica.

Prosta persystencja plikowa (development). W produkcji: baza danych.
"""
from __future__ import annotations

import json
from pathlib import Path

from .config import get_settings
from .presets import default_preset, get_preset


def _profiles_dir() -> Path:
    d = Path(get_settings().data_dir) / "profiles"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path(device_id: str) -> Path:
    return _profiles_dir() / f"{device_id}.json"


def load_raw_profile(device_id: str) -> dict:
    """Zapisane ustawienia urządzenia (bez rozwiniętego presetu)."""
    p = _path(device_id)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    s = get_settings()
    return {
        "preset_id": default_preset()["id"],
        "style": {},
        "language": "pl",
        "extra_instructions": "",
        "provider_profile": s.default_provider_profile,
        "voice": {},
        "parental": {},
        "byok": {},
    }


def save_raw_profile(device_id: str, data: dict) -> dict:
    current = load_raw_profile(device_id)
    current.update({k: v for k, v in data.items() if v is not None})
    _path(device_id).write_text(
        json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return current


def resolve_profile(device_id: str) -> dict:
    """Zwróć profil z osadzonym pełnym presetem (gotowy dla dostawcy AI)."""
    raw = load_raw_profile(device_id)
    preset = get_preset(raw.get("preset_id")) or default_preset()
    profile = dict(raw)
    profile["preset"] = preset
    # provider_profile może pochodzić z presetu, jeśli nie nadpisano w urządzeniu
    profile.setdefault("provider_profile", preset.get("provider_profile", "premium"))
    return profile
