## How it works

This project implements a 4-bit combination lock controlled by a 4x4 matrix keypad. The main modification from a DIP-switch combination lock is that the entered code comes from keypad scanning instead of dedicated switch inputs.

The ASIC drives keypad rows on `uio_out[3:0]` and reads keypad columns on `uio_in[7:4]`. `uio_oe` is fixed at `8'b0000_1111`, so `uio[3:0]` are outputs and `uio[7:4]` are inputs. The visible outputs are `uo_out[0]` for `unlocked`, `uo_out[1]` for `locked_out`, `uo_out[3:2]` for failed attempts, and `uo_out[7:4]` for password/debug bits.

Keypad layout:

```text
Row 0: 1, 2, 3, A
Row 1: 4, 5, 6, B
Row 2: 7, 8, 9, C
Row 3: *, 0, #, D
```

Keys `0` through `9` and `A` through `D` load the current entered 4-bit code. Pressing `*` stores the current entered code as the password. Pressing `#` checks the entered code against the stored password. A correct code asserts `unlocked`; after 3 wrong attempts, `locked_out` becomes active.

## How to test

Run the included template Cocotb test from the repository root:

```sh
make -C test
```

The testbench models the external keypad matrix and verifies reset behavior, `uio_oe`, row scanning, password storage with `*`, password checking with `#`, `unlocked`, and `locked_out` after three wrong attempts.

For hardware testing, connect keypad rows to `uio[3:0]` and keypad columns to `uio[7:4]`. Enter a code such as `5`, press `*` to store it, enter `5` again, and press `#`; `uo_out[0]` should go high. Enter a different code and press `#` three times to make `uo_out[1]` go high.

## External hardware

A 4x4 matrix keypad is required for external input. Optional LEDs or logic analyzer probes can be connected to the output pins to observe `unlocked`, `locked_out`, failed attempts, and password/debug bits.
