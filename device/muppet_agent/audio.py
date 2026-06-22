"""Wejście/wyjście audio (PCM16 mono) na Raspberry Pi przez sounddevice.

- Mikrofon: blok po bloku trafia do kolejki (gdy włączone nagrywanie).
- Głośnik: bufor odtwarzania; w callbacku liczymy głośność i sterujemy buzią.
"""
from __future__ import annotations

import asyncio
import threading

import numpy as np
import sounddevice as sd

from .mouth import Mouth, rms_to_level


class AudioIO:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        sample_rate: int,
        frame_ms: int,
        mouth: Mouth,
        volume: float = 0.8,
    ) -> None:
        self.loop = loop
        self.sample_rate = sample_rate
        self.frame_samples = int(sample_rate * frame_ms / 1000)
        self.mouth = mouth
        self.volume = volume

        self.recording = False
        self.mic_queue: asyncio.Queue[bytes] = asyncio.Queue()

        self._play_buf = bytearray()
        self._play_lock = threading.Lock()

        self._in_stream = sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=self.frame_samples,
            dtype="int16",
            channels=1,
            callback=self._on_input,
        )
        self._out_stream = sd.RawOutputStream(
            samplerate=sample_rate,
            blocksize=self.frame_samples,
            dtype="int16",
            channels=1,
            callback=self._on_output,
        )

    # ── lifecycle ───────────────────────────────────────────────────────
    def start(self) -> None:
        self._in_stream.start()
        self._out_stream.start()

    def stop(self) -> None:
        self._in_stream.stop()
        self._out_stream.stop()
        self.mouth.close()

    # ── mikrofon ────────────────────────────────────────────────────────
    def _on_input(self, indata, frames, time, status) -> None:  # noqa: ANN001
        if not self.recording:
            return
        data = bytes(indata)
        # Przerzuć do pętli asyncio (callback działa w wątku audio).
        self.loop.call_soon_threadsafe(self.mic_queue.put_nowait, data)

    def set_recording(self, value: bool) -> None:
        self.recording = value

    # ── głośnik + buzia ─────────────────────────────────────────────────
    def play(self, pcm: bytes) -> None:
        with self._play_lock:
            self._play_buf.extend(pcm)

    def flush_playback(self) -> None:
        with self._play_lock:
            self._play_buf.clear()
        self.mouth.close()

    def _on_output(self, outdata, frames, time, status) -> None:  # noqa: ANN001
        need = frames * 2  # int16 mono
        with self._play_lock:
            available = min(need, len(self._play_buf))
            chunk = bytes(self._play_buf[:available])
            del self._play_buf[:available]

        if available < need:
            chunk = chunk + b"\x00" * (need - available)  # cisza (dopełnienie)

        samples = np.frombuffer(chunk, dtype=np.int16)
        # Sterowanie buzią głośnością bieżącego bloku.
        level = rms_to_level(samples, self.mouth.sensitivity)
        self.mouth.set_level(level if available > 0 else 0.0)

        # Regulacja głośności (ograniczona dla ochrony słuchu).
        if self.volume != 1.0:
            samples = (samples.astype(np.float32) * self.volume).astype(np.int16)

        outdata[:] = samples.tobytes()
