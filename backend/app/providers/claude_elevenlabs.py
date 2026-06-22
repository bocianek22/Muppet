"""Dostawca PREMIUM: STT (OpenAI Whisper) -> mózg (Claude) -> głos (ElevenLabs).

Niska latencja dzięki strumieniowaniu odpowiedzi Claude zdanie-po-zdaniu wprost
do syntezatora mowy ElevenLabs. Maskotka zaczyna mówić, zanim cała odpowiedź
zostanie wygenerowana.
"""
from __future__ import annotations

import io
import re
import wave

import anthropic
import httpx
from openai import AsyncOpenAI

from ..config import get_settings
from ..presets import build_system_prompt
from .base import Provider, TurnContext

# Granice zdań — punkt, w którym wysyłamy fragment do TTS.
_SENTENCE_END = re.compile(r"[.!?…]+[\s\"')\]]*|\n+")


def _pcm_to_wav(pcm: bytes, sample_rate: int) -> bytes:
    """Opakuj surowy PCM16 mono w kontener WAV (wymagany przez API STT)."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        wav.writeframes(pcm)
    return buf.getvalue()


class ClaudeElevenLabsProvider(Provider):
    name = "premium"

    def __init__(self) -> None:
        s = get_settings()
        self._settings = s
        self._claude = anthropic.AsyncAnthropic(api_key=s.anthropic_api_key)
        self._openai = AsyncOpenAI(api_key=s.openai_api_key)
        self._http = httpx.AsyncClient(timeout=60.0)

    # ── 1. Mowa -> tekst ────────────────────────────────────────────────
    async def _transcribe(self, audio_in: bytes, sample_rate: int) -> str:
        wav = _pcm_to_wav(audio_in, sample_rate)
        resp = await self._openai.audio.transcriptions.create(
            model=self._settings.stt_model,
            file=("speech.wav", wav, "audio/wav"),
        )
        return (resp.text or "").strip()

    # ── 2. Tekst -> mowa (strumieniowo, ElevenLabs) ─────────────────────
    async def _speak(self, text: str, voice: dict, ctx: TurnContext) -> None:
        voice_id = voice.get("voice_id")
        model_id = voice.get("model", "eleven_flash_v2_5")
        url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
            f"?output_format=pcm_{ctx.sample_rate}"
        )
        headers = {
            "xi-api-key": self._settings.elevenlabs_api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
        async with self._http.stream("POST", url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            async for chunk in resp.aiter_bytes():
                if chunk:
                    await ctx.emit_audio(chunk)

    # ── 3. Pełna tura ───────────────────────────────────────────────────
    async def respond(self, ctx: TurnContext) -> None:
        await ctx.emit_event({"type": "state", "value": "transcribing"})
        user_text = await self._transcribe(ctx.audio_in, ctx.sample_rate)
        ctx.user_text = user_text
        await ctx.emit_event({"type": "transcript", "role": "user", "text": user_text})
        if not user_text:
            await ctx.emit_event({"type": "state", "value": "idle"})
            return

        ctx.history.append({"role": "user", "content": user_text})

        system_prompt = build_system_prompt(ctx.profile, ctx.memory.as_prompt_block())
        voice = {
            **ctx.profile["preset"].get("voice", {}),
            **ctx.profile.get("voice", {}),
        }

        await ctx.emit_event({"type": "state", "value": "thinking"})
        await ctx.emit_event({"type": "tts_start", "sample_rate": ctx.sample_rate})

        reply_parts: list[str] = []
        buffer = ""

        # Streaming odpowiedzi Claude. Bez 'thinking' (czat głosowy nie wymaga
        # rozumowania krok po kroku), niski 'effort' -> niska latencja.
        # Aby zwiększyć jakość kosztem latencji: thinking={"type":"adaptive"}.
        async with self._claude.messages.stream(
            model=self._settings.brain_model,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            output_config={"effort": "low"},
            messages=ctx.history,
        ) as stream:
            async for delta in stream.text_stream:
                buffer += delta
                # Wyślij do TTS, gdy uzbiera się całe zdanie.
                while True:
                    match = _SENTENCE_END.search(buffer)
                    if not match:
                        break
                    sentence = buffer[: match.end()].strip()
                    buffer = buffer[match.end():]
                    if sentence:
                        reply_parts.append(sentence)
                        await self._speak(sentence, voice, ctx)

        # Dokończ ostatni, niezakończony fragment.
        tail = buffer.strip()
        if tail:
            reply_parts.append(tail)
            await self._speak(tail, voice, ctx)

        reply_text = " ".join(reply_parts).strip()
        ctx.reply_text = reply_text
        ctx.history.append({"role": "assistant", "content": reply_text})
        await ctx.emit_event({"type": "transcript", "role": "assistant", "text": reply_text})
        await ctx.emit_event({"type": "tts_end"})
        await ctx.emit_event({"type": "state", "value": "idle"})


async def extract_memory(history: list[dict], memory) -> None:
    """W tle: wydobądź trwałe fakty o rozmówcy i zaktualizuj pamięć (tani model).

    Wywoływane fire-and-forget po turze, by nie zwiększać latencji rozmowy.
    """
    import json

    s = get_settings()
    if not s.anthropic_api_key:
        return  # ekstrakcja pamięci wymaga klucza Anthropic (tryb premium)
    client = anthropic.AsyncAnthropic(api_key=s.anthropic_api_key)
    convo = "\n".join(
        f"{m['role']}: {m['content']}" for m in history[-12:] if isinstance(m.get("content"), str)
    )
    try:
        resp = await client.messages.create(
            model=s.memory_model,
            max_tokens=400,
            system=(
                "Wydobądź trwałe, bezpieczne fakty o rozmówcy (np. imię, ulubione "
                "rzeczy, zainteresowania). NIE zapisuj danych wrażliwych (adres, "
                "dane kontaktowe, zdrowie). Zwróć WYŁĄCZNIE JSON: "
                '{"facts": {"klucz": "wartość"}, "summary": "krótkie podsumowanie"}'
            ),
            messages=[{"role": "user", "content": convo or "(brak)"}],
        )
        text = next((b.text for b in resp.content if b.type == "text"), "{}")
        data = json.loads(text)
        if isinstance(data.get("facts"), dict):
            memory.update_facts(data["facts"])
        if isinstance(data.get("summary"), str) and data["summary"]:
            memory.set_summary(data["summary"])
    except Exception:
        # Pamięć jest najlepiej-jak-się-da; błąd nie może psuć rozmowy.
        pass
