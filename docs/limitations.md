# Limitations and next steps

## Current limitations

- The sensor is handmade, so taxel sensitivity and electrode spacing are not perfectly uniform.
- The displayed values are normalized ADC responses rather than calibrated pressure values.
- Hysteresis, drift, repeatability, temperature dependence, and cycle life were not fully characterized.
- Crosstalk was not evaluated with a dedicated controlled comparison.
- Exact physical column indexing in the inherited shift-register firmware requires verification.
- The readout schematic lacks explicit local decoupling capacitors.
- The experiments were bench-top tests and did not demonstrate closed-loop robotic grasp control.

## Recommended next steps

1. Build a single-taxel calibration rig with a load cell and controlled indenter.
2. Measure loading/unloading hysteresis and repeated-cycle drift for representative taxels.
3. Record raw frames instead of only normalized screenshots.
4. Verify row/column mapping with controlled presses at all four corners.
5. Add decoupling capacitors and separate shift/latch control in a new PCB revision.
6. Replace text serial transfer with framed binary packets including a counter and checksum.
7. Integrate the array on a gripper finger and evaluate slip/contact detection during grasping.
