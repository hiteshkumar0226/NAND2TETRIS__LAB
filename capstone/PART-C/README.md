# Capstone — Make the Computer Draw a Box

Personal number: **K = 33** (roll number 2501010133)

- `K mod 3 = 0`: assembler writes all predefined symbols, labels, and variables to `symbols.txt`.
- Box: starts at row 33, is 20 rows tall, and is 32 pixels wide (2 Hack screen words).
- Key pressed: black; key released: white/cleared.

## Run the assembler

```bash
python assembler.py Box.asm
```

This creates `Box.hack` and `symbols.txt`.

## HDL note

The HDL files use standard Nand2Tetris built-in chips for the lower-level components
(e.g. ALU, registers, RAM16K, Screen, Keyboard, ROM32K). If your lab repository has
custom implementations of these chips, keep those files in your repository and use
them in the Hardware Simulator.

## Important validation

Run the official supplied `.tst` files in the Hardware Simulator and CPU Emulator.
The zip does not include the official test scripts or claim that screenshots have
already been captured. Add your own genuine test screenshots to `screenshots/`.
