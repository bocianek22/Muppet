"""Sterowanie ruchem buzi (serwo) oraz diodą stanu.

Działa na Raspberry Pi (gpiozero). Poza Pi przechodzi w tryb zaślepki (mock),
żeby agenta dało się uruchomić na komputerze deweloperskim.
"""
from __future__ import annotations

import math

try:  # Na Raspberry Pi
    from gpiozero import AngularServo, PWMLED  # type: ignore

    _HAS_GPIO = True
except Exception:  # noqa: BLE001 — środowisko bez GPIO (dev)
    _HAS_GPIO = False


class Mouth:
    """Otwiera/zamyka buzię maskotki proporcjonalnie do głośności mowy."""

    def __init__(
        self,
        servo_pin: int,
        closed_value: float = -0.6,
        open_value: float = 0.6,
        sensitivity: float = 4.0,
    ) -> None:
        self.closed = closed_value
        self.open = open_value
        self.sensitivity = sensitivity
        self._level = 0.0
        if _HAS_GPIO:
            # AngularServo używamy w trybie 'value' (-1..1) przez min/max_angle.
            self._servo = AngularServo(
                servo_pin, min_angle=-90, max_angle=90,
                min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000,
            )
        else:
            self._servo = None

    def set_level(self, level: float) -> None:
        """level: 0.0 (cisza/zamknięte) .. 1.0 (głośno/otwarte)."""
        # Wygładzenie, by buzia nie „trzęsła się".
        level = max(0.0, min(1.0, level))
        self._level = 0.5 * self._level + 0.5 * level
        value = self.closed + (self.open - self.closed) * self._level
        if self._servo is not None:
            # AngularServo.angle: -90..90 odpowiada value -1..1
            self._servo.angle = value * 90

    def close(self) -> None:
        self.set_level(0.0)


class StatusLed:
    """Dioda stanu: kolory/jasność sygnalizują tryb pracy."""

    STATES = {
        "idle": 0.15,
        "listening": 1.0,
        "transcribing": 0.5,
        "thinking": 0.5,
        "speaking": 0.8,
        "error": 0.0,
    }

    def __init__(self, led_pin: int) -> None:
        self._led = PWMLED(led_pin) if _HAS_GPIO else None

    def set_state(self, state: str) -> None:
        if self._led is None:
            return
        brightness = self.STATES.get(state, 0.2)
        if state == "thinking":
            self._led.pulse()  # pulsowanie podczas myślenia
        else:
            self._led.value = brightness


def rms_to_level(pcm_int16, sensitivity: float) -> float:
    """Zamień blok PCM16 (numpy int16) na poziom otwarcia buzi 0..1."""
    if len(pcm_int16) == 0:
        return 0.0
    # RMS znormalizowane do zakresu int16, log dla naturalnej reakcji.
    rms = math.sqrt(float((pcm_int16.astype("float32") ** 2).mean()))
    norm = rms / 32768.0
    return max(0.0, min(1.0, norm * sensitivity))
