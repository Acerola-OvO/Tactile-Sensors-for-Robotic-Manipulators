# Firmware

`tactile_sensor_reader.ino` scans a 16×16 matrix using one CD74HC4067 multiplexer and two cascaded SN74HC595 shift registers. The Arduino Nano reads the selected taxel through A0, reduces the 10-bit ADC result to 8 bits, and transmits rows as whitespace-separated integers at 2,000,000 baud.

## Provenance

The firmware is derived from the open-source 3D-ViTac implementation by Binghao Huang. The upstream copyright and MIT license notice remain in the source file. This repository documents its use and adaptation in the graduation-project prototype; it does not claim the scan routine as an original implementation.

## Serial frame format

Each frame contains 16 data rows and one blank delimiter line:

```text
v00 v01 ... v15
v10 v11 ... v15
...
v150 ... v1515

```

## Hardware-verification note

The inherited program clocks the shift register twice before the first ADC sample of each row. Depending on register initialization and physical pin mapping, this may introduce a one-column offset or an inactive final sample. The prototype produced usable heatmaps, but exact column correspondence should be verified with a controlled single-taxel press before quantitative experiments.

## Recommended next revision

- Explicitly clear the cascaded shift registers during startup.
- Separate shift and latch control if the next PCB revision permits it.
- Add a frame counter and checksum or binary packet format.
- Measure and document the real frame rate and end-to-end latency.
