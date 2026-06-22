"""Ładowanie i obsługa presetów (charakterów) maskotki."""
from __future__ import annotations

import json
from pathlib import Path

PRESETS_DIR = Path(__file__).resolve().parent.parent / "presets"


def load_presets() -> list[dict]:
    """Wczytaj wszystkie presety z katalogu backend/presets/*.json."""
    presets: list[dict] = []
    for path in sorted(PRESETS_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as fh:
            presets.append(json.load(fh))
    return presets


def get_preset(preset_id: str) -> dict | None:
    for preset in load_presets():
        if preset.get("id") == preset_id:
            return preset
    return None


def default_preset() -> dict:
    presets = load_presets()
    if not presets:
        raise RuntimeError("Brak presetów w backend/presets/")
    return presets[0]


def build_system_prompt(profile: dict, memory_block: str) -> str:
    """Zbuduj prompt systemowy z presetu + dostrojeń + pamięci egzemplarza.

    Zwracany tekst jest STABILNY w obrębie urządzenia (poza blokiem pamięci),
    co pozwala backendowi korzystać z prompt caching (patrz claude_elevenlabs.py).
    """
    preset = profile["preset"]
    style = {**preset.get("style", {}), **profile.get("style", {})}
    safety = preset.get("safety", {})
    language = profile.get("language", preset.get("language", "pl"))

    blocked = ", ".join(safety.get("blocked_topics", [])) or "brak"
    extra = profile.get("extra_instructions", "").strip()

    return (
        f"{preset['system_prompt']}\n\n"
        f"# Zasady rozmowy\n"
        f"- Język odpowiedzi: {language}.\n"
        f"- Mówisz na głos przez głośnik maskotki — odpowiadaj krótko, naturalnie,\n"
        f"  pełnymi zdaniami, bez znaczników, emoji i list. Maks. 2-3 zdania,\n"
        f"  chyba że dziecko prosi o dłuższą historię.\n"
        f"- Styl: energia={style.get('energy', 0.6)}, humor={style.get('humor', 0.5)},\n"
        f"  gadatliwość={style.get('verbosity', 0.4)}.\n"
        f"# Bezpieczeństwo (rozmowa z dzieckiem)\n"
        f"- Grupa wiekowa: {preset.get('age_range', 'dzieci')}.\n"
        f"- Tematy zabronione: {blocked}.\n"
        f"- Gdy temat jest nieodpowiedni: {safety.get('refusal_style', 'łagodnie zmień temat')}.\n"
        f"- Nigdy nie proś o dane osobowe, adres, hasła; nie zachęcaj do działań ryzykownych.\n"
        + (f"# Dodatkowe wskazówki od opiekuna\n{extra}\n" if extra else "")
        + f"# Co już wiesz o tym dziecku/rozmówcy (pamięć)\n{memory_block}\n"
    )
