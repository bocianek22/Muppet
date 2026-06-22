"""Abstrakcja dostawców AI: 'base' (OpenAI Realtime) i 'premium' (Claude+ElevenLabs).

Wybór profilu odbywa się per-urządzenie/per-preset i może być zmieniony z
aplikacji bez aktualizacji firmware'u.
"""
from __future__ import annotations

from .base import Provider, TurnContext


def get_provider(profile_name: str) -> Provider:
    if profile_name == "base":
        from .openai_provider import OpenAIProvider

        return OpenAIProvider()
    # domyślnie premium
    from .claude_elevenlabs import ClaudeElevenLabsProvider

    return ClaudeElevenLabsProvider()


__all__ = ["Provider", "TurnContext", "get_provider"]
