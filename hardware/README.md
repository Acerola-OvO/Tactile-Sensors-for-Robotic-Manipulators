# Hardware

The prototype combines a handmade 16×16 Velostat pressure matrix with a reading board built around an Arduino Nano, one CD74HC4067 16-channel multiplexer, and two cascaded SN74HC595 shift registers.

## Directory contents

- `schematics/sensor_reading_board_redrawn.pdf`: schematic redrawn in JLCEDA for this graduation project.
- `manufacturing/reading-board/`: Gerber and pick-and-place files for the main readout PCB.
- `manufacturing/connector-board/`: Gerber and pick-and-place files for the sensor connector PCB.
- `bom/`: UTF-8 BOM files converted from the manufacturing exports.

## Attribution

The circuit topology and manufacturing design are based on the 3D-ViTac tactile sensing reference hardware. The schematic was redrawn and documented for this project. The repository does not present the underlying circuit topology as an independently invented design.

## Design review notes

The present schematic reproduces the working prototype, but a future revision should add local 100 nF decoupling capacitors for the CD74HC4067 and each SN74HC595, plus a bulk capacitor near the board power input. Exact FPC orientation and row/column polarity should be checked before ordering.
