# Sensor fabrication

The tactile sensing sheet is a handmade 16×16 piezoresistive matrix fabricated
from flexible materials and connected to an external readout board.

This page summarizes the fabrication materials, the layered sensor structure,
and the main assembly steps used in the graduation-project prototype.

---

## Materials

The following materials were used for the sensor body:

- Velostat sheet as the piezoresistive sensing layer
- Polyimide film as the flexible substrate
- Conductive electrodes arranged in orthogonal row and column directions
- Adhesive layer for structural fixation
- Flexible connector tabs for interfacing with the readout board
- External sensor-reading PCB and Arduino Nano for data acquisition

---

## Layered sensor structure

The sensor consists of stacked flexible layers. The Velostat sheet is sandwiched
between orthogonal row and column electrodes so that local pressure changes the
contact resistance at each intersection.

<p align="center">
  <img src="../assets/fabrication_docs/layered_structure.png"
       alt="Layered structure of the tactile sensor"
       width="520">
</p>

<p align="center">
  <em>
    Figure 1. Conceptual layered structure of the handmade flexible tactile sensor.
  </em>
</p>

---

## Fabrication procedure

The prototype was fabricated through the following steps.

### Step 1. Prepare the Velostat sensing layer

A square Velostat sheet was cut to the target sensing size and used as the
piezoresistive core layer of the tactile sensor.

<p align="center">
  <img src="../assets/fabrication_docs/velostat_layer.jpg"
       alt="Velostat sensing layer"
       width="320">
</p>

<p align="center">
  <em>Figure 2. Cut Velostat sensing layer.</em>
</p>

### Step 2. Prepare the polyimide base

A polyimide base layer was prepared to support the flexible electrode structure
and the connector interfaces.

<p align="center">
  <img src="../assets/fabrication_docs/polyimide_base.jpg"
       alt="Polyimide base"
       width="420">
</p>

<p align="center">
  <em>Figure 3. Polyimide base and flexible electrode interface area.</em>
</p>

### Step 3. Apply the adhesive layer

An adhesive layer was added to mechanically stabilize the sensor stack and
maintain alignment between the functional layers.

<p align="center">
  <img src="../assets/fabrication_docs/adhesive_layer.jpg"
       alt="Adhesive layer"
       width="420">
</p>

<p align="center">
  <em>Figure 4. Adhesive layer used for structural fixation.</em>
</p>

### Step 4. Align the electrode array

The row and column electrodes were arranged orthogonally. Their overlap defined
the 16×16 taxel matrix.

<p align="center">
  <img src="../assets/fabrication_docs/electrode_alignment.jpg"
       alt="Electrode alignment"
       width="420">
</p>

<p align="center">
  <em>
    Figure 5. Electrode alignment before final lamination of the tactile matrix.
  </em>
</p>

### Step 5. Assemble the tactile sensor

After the layers were aligned, the complete flexible sensor was laminated into
a finished 16×16 tactile array with connector tabs for readout.

<p align="center">
  <img src="../assets/fabrication_docs/assembled_sensor.jpg"
       alt="Assembled tactile sensor"
       width="320">
</p>

<p align="center">
  <em>Figure 6. Finished 16×16 flexible tactile sensor.</em>
</p>

### Step 6. Connect the sensor to the readout board

The completed sensor was connected to the external readout system consisting of
the sensor-reading board and Arduino Nano.

<p align="center">
  <img src="../assets/fabrication_docs/sensor_readout_board.jpg"
       alt="Sensor and readout board"
       width="420">
</p>

<p align="center">
  <em>
    Figure 7. Finished sensor connected to the Arduino-based readout board.
  </em>
</p>

---

## Final prototype

The final prototype combines the handmade flexible sensing sheet with the
external scanning and acquisition hardware. This configuration was then used
for the pressure-range, spatial-response, and small-object contact experiments
described in [experiments.md](experiments.md).

---

## Notes and limitations

- The sensor was handmade, so taxel uniformity is limited.
- Alignment accuracy directly affects sensitivity consistency.
- The fabrication process emphasizes low cost and ease of prototyping rather
  than industrial manufacturing precision.
- The current repository documents the prototype fabrication workflow rather
  than a mass-production-ready process.
