"""Wspólny interfejs dostawców i kontekst tury rozmowy."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Awaitable, Callable

from ..memory import DeviceMemory


@dataclass
class TurnContext:
    """Wszystko, czego dostawca potrzebuje do obsłużenia jednej tury rozmowy."""

    audio_in: bytes                       # PCM16 mono (sample_rate wg configu)
    sample_rate: int
    profile: dict                         # {preset, style, language, extra_instructions, ...}
    memory: DeviceMemory
    history: list[dict]                   # współdzielona historia rozmowy (mutowana)

    # Wyjście do urządzenia:
    emit_audio: Callable[[bytes], Awaitable[None]]   # binarny PCM16 do odtworzenia
    emit_event: Callable[[dict], Awaitable[None]]    # JSON: state/transcript/tts_start/...

    # Wypełniane przez dostawcę (do logów/pamięci):
    user_text: str = ""
    reply_text: str = ""
    meta: dict = field(default_factory=dict)


class Provider(ABC):
    """Dostawca realizuje pełną turę: audio wejściowe -> audio wyjściowe."""

    name: str = "base"

    @abstractmethod
    async def respond(self, ctx: TurnContext) -> None:
        """Przetwórz audio wejściowe i wyemituj odpowiedź (audio + zdarzenia)."""
        raise NotImplementedError
