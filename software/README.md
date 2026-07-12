# Visualization software

The visualizer reads 16 rows of 16 integer samples followed by a blank line. It performs per-taxel median baseline calibration, threshold subtraction, optional Gaussian smoothing, exponential moving average smoothing, and OpenCV heatmap rendering.

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r software/requirements.txt
```

## Run with hardware

```bash
python software/tactile_visualizer.py --port COM5
# or
python software/tactile_visualizer.py --port /dev/ttyUSB0
```

The firmware uses 2,000,000 baud by default. Keep the sensor unloaded during the first 30 frames while the baseline is measured.

## Run without hardware

```bash
python software/tactile_visualizer.py --simulate
```

Use `--help` to see filtering, normalization, and array-size options. The `per-frame` normalization mode resembles the legacy prototype display but should not be interpreted as calibrated pressure.
