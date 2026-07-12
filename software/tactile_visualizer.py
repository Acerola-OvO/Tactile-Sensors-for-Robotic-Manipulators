"""Real-time visualizer for the 16x16 tactile sensor prototype."""
from __future__ import annotations

import argparse
import queue
import sys
import threading
import time
from dataclasses import dataclass
from typing import Iterator, Optional

import cv2
import numpy as np
import serial
from serial.tools import list_ports

from tactile_core import (
    FrameAssembler,
    FrameFormatError,
    ProcessorConfig,
    TactileProcessor,
    median_baseline,
)


@dataclass
class ReaderStats:
    valid_frames: int = 0
    malformed_frames: int = 0


def available_ports() -> list[str]:
    return [port.device for port in list_ports.comports()]


def resolve_port(requested: str) -> str:
    if requested != "auto":
        return requested
    ports = available_ports()
    if not ports:
        raise RuntimeError("No serial ports detected. Pass --port explicitly.")
    if len(ports) > 1:
        joined = ", ".join(ports)
        raise RuntimeError(f"Multiple serial ports detected ({joined}); pass --port.")
    return ports[0]


def serial_frames(
    device: serial.Serial,
    rows: int,
    columns: int,
    stop_event: threading.Event,
    stats: ReaderStats,
) -> Iterator[np.ndarray]:
    assembler = FrameAssembler(rows, columns)
    while not stop_event.is_set():
        raw = device.readline()
        if not raw:
            continue
        try:
            line = raw.decode("utf-8", errors="strict")
            frame = assembler.push(line)
        except (UnicodeDecodeError, FrameFormatError) as exc:
            stats.malformed_frames += 1
            print(f"[serial warning] {exc}", file=sys.stderr)
            continue
        if frame is not None:
            stats.valid_frames += 1
            yield frame


def simulated_frames(rows: int, columns: int, stop_event: threading.Event) -> Iterator[np.ndarray]:
    """Generate a moving synthetic contact spot for software-only testing."""
    yy, xx = np.mgrid[0:rows, 0:columns]
    step = 0
    while not stop_event.is_set():
        center_x = (columns - 1) * (0.5 + 0.38 * np.sin(step / 25.0))
        center_y = (rows - 1) * (0.5 + 0.38 * np.cos(step / 31.0))
        spot = 85.0 * np.exp(-((xx - center_x) ** 2 + (yy - center_y) ** 2) / 3.0)
        noise = np.random.default_rng(step).normal(0.0, 1.5, size=(rows, columns))
        yield (20.0 + spot + noise).astype(np.float32)
        step += 1
        time.sleep(0.03)


def reader_worker(
    output: queue.Queue[np.ndarray],
    stop_event: threading.Event,
    source: Iterator[np.ndarray],
) -> None:
    try:
        for frame in source:
            if stop_event.is_set():
                break
            try:
                output.put(frame, timeout=0.1)
            except queue.Full:
                try:
                    output.get_nowait()
                except queue.Empty:
                    pass
                output.put_nowait(frame)
    except Exception as exc:  # propagate operational failures to stderr
        print(f"[reader error] {exc}", file=sys.stderr)
        stop_event.set()


def render_heatmap(data: np.ndarray, scale: int) -> np.ndarray:
    display = np.clip(data * 255.0, 0, 255).astype(np.uint8)
    colored = cv2.applyColorMap(display, cv2.COLORMAP_VIRIDIS)
    return cv2.resize(
        colored,
        (data.shape[1] * scale, data.shape[0] * scale),
        interpolation=cv2.INTER_NEAREST,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="auto", help="Serial port, e.g. COM5 or /dev/ttyUSB0")
    parser.add_argument("--baud", type=int, default=2_000_000)
    parser.add_argument("--rows", type=int, default=16)
    parser.add_argument("--columns", type=int, default=16)
    parser.add_argument("--baseline-frames", type=int, default=30)
    parser.add_argument("--threshold", type=float, default=12.0)
    parser.add_argument("--clip-max", type=float, default=100.0)
    parser.add_argument("--ema-alpha", type=float, default=0.2)
    parser.add_argument("--gaussian-sigma", type=float, default=0.0)
    parser.add_argument(
        "--normalization",
        choices=("fixed", "per-frame", "none"),
        default="fixed",
    )
    parser.add_argument("--scale", type=int, default=30)
    parser.add_argument("--simulate", action="store_true", help="Run without hardware")
    parser.add_argument("--list-ports", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.list_ports:
        ports = available_ports()
        print("\n".join(ports) if ports else "No serial ports detected")
        return 0

    stop_event = threading.Event()
    frame_queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=3)
    stats = ReaderStats()
    device: Optional[serial.Serial] = None

    if args.simulate:
        source = simulated_frames(args.rows, args.columns, stop_event)
    else:
        port = resolve_port(args.port)
        print(f"Opening {port} at {args.baud} baud")
        device = serial.Serial(port, args.baud, timeout=0.2)
        device.reset_input_buffer()
        source = serial_frames(device, args.rows, args.columns, stop_event, stats)

    thread = threading.Thread(
        target=reader_worker,
        args=(frame_queue, stop_event, source),
        daemon=True,
    )
    thread.start()

    try:
        calibration: list[np.ndarray] = []
        print(f"Collecting {args.baseline_frames} baseline frames. Keep the sensor unloaded.")
        while len(calibration) < args.baseline_frames and not stop_event.is_set():
            try:
                calibration.append(frame_queue.get(timeout=1.0))
            except queue.Empty:
                print("Waiting for complete frames...", file=sys.stderr)

        if stop_event.is_set() or not calibration:
            raise RuntimeError("Reader stopped before baseline calibration completed")

        baseline = median_baseline(calibration)
        processor = TactileProcessor(
            baseline,
            ProcessorConfig(
                threshold=args.threshold,
                clip_max=args.clip_max,
                ema_alpha=args.ema_alpha,
                gaussian_sigma=args.gaussian_sigma,
                normalization=args.normalization,
            ),
        )

        window = "16x16 Tactile Sensor - press Q or Esc to exit"
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        last_report = time.monotonic()
        displayed = 0

        while not stop_event.is_set():
            try:
                frame = frame_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            processed = processor.process(frame)
            cv2.imshow(window, render_heatmap(processed, args.scale))
            displayed += 1
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break

            now = time.monotonic()
            if now - last_report >= 2.0:
                print(
                    f"displayed={displayed}, valid_serial_frames={stats.valid_frames}, "
                    f"malformed={stats.malformed_frames}"
                )
                last_report = now

    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        if device is not None and device.is_open:
            device.close()
        cv2.destroyAllWindows()
        thread.join(timeout=1.0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
