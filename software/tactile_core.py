"""Core parsing and signal-processing utilities for a 16x16 tactile array.

The serial frame format follows the prototype firmware used in this project:
16 whitespace-separated integer rows followed by a blank line.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

import numpy as np
from scipy.ndimage import gaussian_filter


class FrameFormatError(ValueError):
    """Raised when a serial row or frame does not match the expected shape."""


def parse_row(line: str, columns: int = 16) -> Optional[np.ndarray]:
    """Parse one whitespace-separated sensor row.

    Returns ``None`` for a blank line, which acts as a frame delimiter.
    """
    stripped = line.strip()
    if not stripped:
        return None

    try:
        values = np.asarray([int(token) for token in stripped.split()], dtype=np.float32)
    except ValueError as exc:
        raise FrameFormatError(f"Non-integer value in row: {line!r}") from exc

    if values.size != columns:
        raise FrameFormatError(
            f"Expected {columns} values, received {values.size}: {line!r}"
        )
    return values


class FrameAssembler:
    """Assemble row strings into complete tactile frames."""

    def __init__(self, rows: int = 16, columns: int = 16) -> None:
        self.rows = rows
        self.columns = columns
        self._current: list[np.ndarray] = []

    def push(self, line: str) -> Optional[np.ndarray]:
        row = parse_row(line, self.columns)
        if row is None:
            if not self._current:
                return None
            if len(self._current) != self.rows:
                received = len(self._current)
                self._current.clear()
                raise FrameFormatError(
                    f"Incomplete frame: expected {self.rows} rows, received {received}"
                )
            frame = np.stack(self._current, axis=0)
            self._current.clear()
            return frame

        if len(self._current) >= self.rows:
            self._current.clear()
            raise FrameFormatError("Frame contains too many rows before delimiter")

        self._current.append(row)
        return None


@dataclass
class ProcessorConfig:
    threshold: float = 12.0
    clip_max: float = 100.0
    ema_alpha: float = 0.2
    gaussian_sigma: float = 0.0
    normalization: str = "fixed"  # fixed, per-frame, or none


class TactileProcessor:
    """Baseline subtraction, denoising, smoothing, and display normalization."""

    def __init__(self, baseline: np.ndarray, config: ProcessorConfig) -> None:
        baseline = np.asarray(baseline, dtype=np.float32)
        if baseline.ndim != 2:
            raise ValueError("Baseline must be a 2D array")
        if not 0.0 < config.ema_alpha <= 1.0:
            raise ValueError("ema_alpha must be in the interval (0, 1]")
        if config.clip_max <= 0:
            raise ValueError("clip_max must be positive")
        if config.normalization not in {"fixed", "per-frame", "none"}:
            raise ValueError("normalization must be fixed, per-frame, or none")

        self.baseline = baseline
        self.config = config
        self._previous = np.zeros_like(baseline, dtype=np.float32)

    def process(self, frame: np.ndarray) -> np.ndarray:
        frame = np.asarray(frame, dtype=np.float32)
        if frame.shape != self.baseline.shape:
            raise ValueError(
                f"Frame shape {frame.shape} does not match baseline {self.baseline.shape}"
            )

        contact = frame - self.baseline - self.config.threshold
        contact = np.clip(contact, 0.0, self.config.clip_max)

        if self.config.gaussian_sigma > 0:
            contact = gaussian_filter(contact, sigma=self.config.gaussian_sigma)

        alpha = self.config.ema_alpha
        smoothed = alpha * contact + (1.0 - alpha) * self._previous
        self._previous = smoothed

        if self.config.normalization == "none":
            return smoothed
        if self.config.normalization == "fixed":
            return np.clip(smoothed / self.config.clip_max, 0.0, 1.0)

        frame_max = float(np.max(smoothed))
        if frame_max <= 0:
            return np.zeros_like(smoothed)
        return np.clip(smoothed / frame_max, 0.0, 1.0)


def median_baseline(frames: Iterable[np.ndarray]) -> np.ndarray:
    """Compute a per-taxel median baseline from calibration frames."""
    stack = np.asarray(list(frames), dtype=np.float32)
    if stack.ndim != 3 or stack.shape[0] == 0:
        raise ValueError("At least one 2D calibration frame is required")
    return np.median(stack, axis=0)
