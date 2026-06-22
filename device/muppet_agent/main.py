"""Główny agent urządzenia: spina przycisk, audio, buzię i połączenie z backendem.

Przepływ (push-to-talk):
  wciśnięcie przycisku  -> audio_start + strumień ramek mikrofonu do backendu
  zwolnienie przycisku  -> audio_end (backend przetwarza i odsyła głos)
  odbiór ramek audio    -> odtwarzanie + ruch buzi
"""
from __future__ import annotations

import argparse
import asyncio
import json
import signal

import yaml

try:
    from gpiozero import Button  # type: ignore

    _HAS_GPIO = True
except Exception:  # noqa: BLE001
    _HAS_GPIO = False

import websockets

from .audio import AudioIO
from .mouth import Mouth, StatusLed


class Agent:
    def __init__(self, config: dict) -> None:
        self.cfg = config
        self.loop = asyncio.get_event_loop()
        pins = config["pins"]
        m = config.get("mouth", {})
        self.mouth = Mouth(
            pins["servo"],
            closed_value=m.get("closed_value", -0.6),
            open_value=m.get("open_value", 0.6),
            sensitivity=m.get("sensitivity", 4.0),
        )
        self.led = StatusLed(pins["led"])
        self.audio = AudioIO(
            self.loop,
            sample_rate=config["sample_rate"],
            frame_ms=config["frame_ms"],
            mouth=self.mouth,
            volume=min(config.get("volume", 0.8), config.get("max_volume", 0.9)),
        )
        self.ws: websockets.WebSocketClientProtocol | None = None
        self._recording = False
        self._send_task: asyncio.Task | None = None

        if _HAS_GPIO and config.get("push_to_talk", True):
            self.button = Button(pins["button"], pull_up=True, bounce_time=0.05)
            self.button.when_pressed = lambda: self.loop.call_soon_threadsafe(
                self._start_recording
            )
            self.button.when_released = lambda: self.loop.call_soon_threadsafe(
                self._stop_recording
            )
        else:
            self.button = None

    # ── nagrywanie (push-to-talk) ───────────────────────────────────────
    def _start_recording(self) -> None:
        if self._recording or self.ws is None:
            return
        self._recording = True
        self.led.set_state("listening")
        self.audio.flush_playback()  # przerwij ewentualne odtwarzanie (barge-in)
        self.audio.set_recording(True)
        self._send_task = self.loop.create_task(self._stream_mic())

    def _stop_recording(self) -> None:
        if not self._recording:
            return
        self._recording = False
        self.audio.set_recording(False)
        self.loop.create_task(self._send_json({"type": "audio_end"}))

    async def _stream_mic(self) -> None:
        await self._send_json({"type": "audio_start"})
        while self._recording:
            try:
                frame = await asyncio.wait_for(self.audio.mic_queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue
            if self.ws is not None:
                await self.ws.send(frame)
        # opróżnij resztę bufora mikrofonu
        while not self.audio.mic_queue.empty():
            frame = self.audio.mic_queue.get_nowait()
            if self.ws is not None:
                await self.ws.send(frame)

    # ── komunikacja z backendem ─────────────────────────────────────────
    async def _send_json(self, obj: dict) -> None:
        if self.ws is not None:
            await self.ws.send(json.dumps(obj))

    async def _handle_event(self, event: dict) -> None:
        etype = event.get("type")
        if etype == "state":
            self.led.set_state(event.get("value", "idle"))
        elif etype == "tts_start":
            self.led.set_state("speaking")
        elif etype == "tts_end":
            self.led.set_state("idle")
        elif etype == "profile":
            print("[profil]", event)
        elif etype == "transcript":
            print(f"[{event.get('role')}] {event.get('text')}")
        elif etype == "error":
            print("[BŁĄD backendu]", event.get("message"))
            self.led.set_state("error")

    async def _receive_loop(self) -> None:
        assert self.ws is not None
        async for message in self.ws:
            if isinstance(message, (bytes, bytearray)):
                self.audio.play(bytes(message))  # ramka audio TTS
            else:
                await self._handle_event(json.loads(message))

    # ── pętla połączenia (z reconnectem) ────────────────────────────────
    async def run(self) -> None:
        self.audio.start()
        self.led.set_state("idle")
        url = self.cfg["backend_url"]
        headers = {"Authorization": f"Bearer {self.cfg['device_token']}"}
        while True:
            try:
                # Nazwa parametru nagłówków różni się między wersjami websockets:
                # >=13 -> additional_headers, <=12 -> extra_headers.
                try:
                    connect_cm = websockets.connect(
                        url, additional_headers=headers, max_size=None
                    )
                except TypeError:
                    connect_cm = websockets.connect(
                        url, extra_headers=headers, max_size=None
                    )
                async with connect_cm as ws:
                    self.ws = ws
                    await self._send_json({"type": "hello"})
                    print("[połączono z backendem]")
                    await self._receive_loop()
            except Exception as exc:  # noqa: BLE001 — reconnect
                print("[rozłączono]", exc)
                self.led.set_state("error")
            finally:
                self.ws = None
            await asyncio.sleep(3)  # backoff przed ponownym połączeniem

    def shutdown(self) -> None:
        self.audio.stop()


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent urządzenia Muppet AI")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    agent = Agent(config)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, loop.stop)

    try:
        loop.run_until_complete(agent.run())
    finally:
        agent.shutdown()


if __name__ == "__main__":
    main()
