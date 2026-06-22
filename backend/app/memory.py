"""Pamięć długoterminowa egzemplarza maskotki (per device_id).

Prosta implementacja plikowa na potrzeby developmentu. W produkcji zastąp bazą
danych (Postgres) z szyfrowaniem w spoczynku i politykami retencji (RODO).
"""
from __future__ import annotations

import json
from pathlib import Path

from .config import get_settings


class DeviceMemory:
    """Pamięć pojedynczego urządzenia: trwałe fakty + krótkie podsumowanie."""

    def __init__(self, device_id: str) -> None:
        self.device_id = device_id
        base = Path(get_settings().data_dir) / "memory"
        base.mkdir(parents=True, exist_ok=True)
        self.path = base / f"{device_id}.json"
        self.data: dict = {"facts": {}, "summary": ""}
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass

    def as_prompt_block(self) -> str:
        facts = self.data.get("facts", {})
        summary = self.data.get("summary", "")
        if not facts and not summary:
            return "(jeszcze nic — to może być pierwsza rozmowa)"
        lines = []
        if facts:
            lines.append("Fakty: " + "; ".join(f"{k}: {v}" for k, v in facts.items()))
        if summary:
            lines.append("Podsumowanie wcześniejszych rozmów: " + summary)
        return "\n".join(lines)

    def update_facts(self, new_facts: dict) -> None:
        self.data.setdefault("facts", {}).update(new_facts)
        self._save()

    def set_summary(self, summary: str) -> None:
        self.data["summary"] = summary
        self._save()

    def clear(self) -> None:
        self.data = {"facts": {}, "summary": ""}
        self._save()

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
