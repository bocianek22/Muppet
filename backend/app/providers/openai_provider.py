"""Dostawca BAZOWY: cały tor mowa->rozum->mowa na JEDNYM kluczu OpenAI.

To realizacja zasady „działa na jednej licencji". Używa standardowych API OpenAI:
  - STT:  audio.transcriptions  (np. whisper-1 / gpt-4o-transcribe)
  - rozum: chat.completions     (np. gpt-4o-mini) — strumieniowo
  - TTS:  audio.speech          (np. gpt-4o-mini-tts) — format PCM

Dzięki strumieniowaniu odpowiedzi zdanie-po-zdaniu latencja jest niska.

> Dla ABSOLUTNIE najniższej latencji można zamiast tego podłączyć właściwe
> OpenAI Realtime API (WebSocket, speech-to-speech w jednym strumieniu). Wymaga
> to mostkowania audio i resamplingu do formatu Realtime — zostawiamy jako
> rozszerzenie; ten potok jest prostszy i wystarczający na start.
"""
from __future__ import annotations

import io
import re
import wave

from openai import AsyncOpenAI

from ..config import get_settings
from ..presets import build_system_prompt
from .base import Provider, TurnContext

_SENTENCE_END = re.compile(r"[.!?…]+[\s\"')\]]*|\n+")


def _pcm_to_wav(pcm: bytes, sample_rate: int) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm)
    return buf.getvalue()


class OpenAIProvider(Provider):
    name = "base"

    def __init__(self) -> None:
        s = get_settings()
        self._settings = s
        self._client = AsyncOpenAI(api_key=s.openai_api_key)
        # Modele bazowe — możesz nadpisać w presecie (voice.openai_*).
        self._stt = s.stt_model
        self._chat = "gpt-4o-mini"
        self._tts = "gpt-4o-mini-tts"

    async def _transcribe(self, audio_in: bytes, sample_rate: int) -> str:
        wav = _pcm_to_wav(audio_in, sample_rate)
        resp = await self._client.audio.transcriptions.create(
            model=self._stt, file=("speech.wav", wav, "audio/wav")
        )
        return (resp.text or "").strip()

    async def _speak(self, text: str, voice_name: str, ctx: TurnContext) -> None:
        # Surowy PCM16 zgodny z urządzeniem (response_format="pcm" = 24kHz w OpenAI;
        # jeśli różni się od sample_rate urządzenia, ustaw resampling po stronie
        # urządzenia lub backendu). Tu zakładamy zgodny strumień PCM16 mono.
        async with self._client.audio.speech.with_streaming_response.create(
            model=self._tts,
            voice=voice_name,
            input=text,
            response_format="pcm",
        ) as resp:
            async for chunk in resp.iter_bytes():
                if chunk:
                    await ctx.emit_audio(chunk)

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
        voice_name = (
            ctx.profile.get("voice", {}).get("openai_voice")
            or ctx.profile["preset"].get("voice", {}).get("openai_realtime_voice")
            or "alloy"
        )

        await ctx.emit_event({"type": "state", "value": "thinking"})
        await ctx.emit_event({"type": "tts_start", "sample_rate": ctx.sample_rate})

        messages = [{"role": "system", "content": system_prompt}, *ctx.history]
        reply_parts: list[str] = []
        buffer = ""

        stream = await self._client.chat.completions.create(
            model=self._chat, messages=messages, max_tokens=400, stream=True
        )
        async for event in stream:
            delta = event.choices[0].delta.content or ""
            if not delta:
                continue
            buffer += delta
            while True:
                match = _SENTENCE_END.search(buffer)
                if not match:
                    break
                sentence = buffer[: match.end()].strip()
                buffer = buffer[match.end():]
                if sentence:
                    reply_parts.append(sentence)
                    await self._speak(sentence, voice_name, ctx)

        tail = buffer.strip()
        if tail:
            reply_parts.append(tail)
            await self._speak(tail, voice_name, ctx)

        reply_text = " ".join(reply_parts).strip()
        ctx.reply_text = reply_text
        ctx.history.append({"role": "assistant", "content": reply_text})
        await ctx.emit_event({"type": "transcript", "role": "assistant", "text": reply_text})
        await ctx.emit_event({"type": "tts_end"})
        await ctx.emit_event({"type": "state", "value": "idle"})
