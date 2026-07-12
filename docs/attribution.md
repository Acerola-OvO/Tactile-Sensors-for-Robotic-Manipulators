# Attribution and scope of contribution

This repository documents a graduation-project reproduction and experimental adaptation of a low-cost flexible tactile sensor.

## Upstream work

The reference scan firmware, reading-board topology, and material approach were based on the open-source **3D-ViTac: Learning Fine-Grained Manipulation with Visuo-Tactile Sensing** project by Binghao Huang and collaborators.

The Arduino source retains the upstream copyright and MIT license notice.

## Work documented in this repository

- Fabrication of a handmade 16×16 Velostat tactile array
- Assembly and integration of the sensor, readout electronics, and host computer
- Redrawing and documentation of the readout schematic in JLCEDA
- Adaptation and cleanup of the Python visualization workflow
- Baseline subtraction, thresholding, temporal smoothing, and optional spatial smoothing
- Bench-top experiments using calibrated weights and small objects
- Organization of manufacturing files, documentation, and reproducibility notes

## Scope statement

This project does not claim that the reference circuit topology or original firmware was invented from scratch. Its value lies in reproducing the complete sensing pipeline, understanding the hardware/software interface, fabricating the sensor, and evaluating the resulting prototype.
