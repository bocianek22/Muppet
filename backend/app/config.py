"""Konfiguracja backendu — wczytywana ze zmiennych środowiskowych / .env."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Klucze dostawców (licencja właściciela)
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    elevenlabs_api_key: str = ""
    gemini_api_key: str = ""

    # Domyślny profil dostawcy: "base" | "premium"
    default_provider_profile: str = "premium"

    # Modele
    brain_model: str = "claude-opus-4-8"
    memory_model: str = "claude-haiku-4-5"
    stt_model: str = "whisper-1"

    # Audio na linii urządzenie<->backend (PCM16 mono)
    audio_sample_rate: int = 16000

    # Bezpieczeństwo / dane
    jwt_secret: str = "zmien-mnie-w-produkcji"
    data_dir: str = "./data"


@lru_cache
def get_settings() -> Settings:
    return Settings()
