## How it works

This project implements a 4-bit digital combination lock using a 4x4 matrix keypad as the user input interface.

The design is based on a TinyTapeout-style Combination Lock. The main functional modification is that the password is no longer entered using DIP switches. Instead, a typical Arduino-style 4x4 matrix keypad is scanned through the bidirectional `uio` pins.

The keypad rows are driven by the ASIC through `uio_out[3:0]`, and the keypad columns are read by the ASIC through `uio_in[7:4]`. The output enable value is `uio_oe = 8'b0000_1111`, so the lower four `uio` pins are outputs and the upper four `uio` pins are inputs.

Keypad layout:

```text
Row 0: 1, 2, 3, A
Row 1: 4, 5, 6, B
Row 2: 7, 8, 9, C
Row 3: *, 0, #, D## How it works

This project implements a 4-bit combination lock controlled by a 4x4 matrix keypad. The ASIC drives the four keypad rows on `uio_out[3:0]` as active-low scan outputs and reads the four keypad columns on `uio_in[7:4]` as active-low inputs. `uio_oe` is fixed at `8'b0000_1111`, making `uio[3:0]` outputs and `uio[7:4]` inputs.

The keypad layout is:

|       | Col 0 | Col 1 | Col 2 | Col 3 |
| ----- | ----- | ----- | ----- | ----- |
| Row 0 | 1     | 2     | 3     | A     |
| Row 1 | 4     | 5     | 6     | B     |
| Row 2 | 7     | 8     | 9     | C     |
| Row 3 | *     | 0     | #     | D     |

Keys `0` through `9` and `A` through `D` load the current entered 4-bit code. Pressing `*` stores the current entered code as the password and clears the failed-attempt count. Pressing `#` checks the current entered code against the stored password. A correct code asserts `uo_out[0]` (`unlocked`). Each wrong `#` check increments the failed-attempt count on `uo_out[3:2]`; after three wrong attempts, `uo_out[1]` (`locked_out`) becomes active.

The upper output nibble, `uo_out[7:4]`, exposes the stored password/debug bits for bring-up and demonstration.

## How to test

Connect a 4x4 matrix keypad to the bidirectional pins with rows on `uio[3:0]` and columns on `uio[7:4]`. The row pins are active-low outputs from the ASIC, and the column pins should be read as active-low inputs when a key connects the selected row to a column.

After reset, enter a code key such as `5`, press `*` to store it as the password, then enter `5` again and press `#`. `uo_out[0]` should go high. Enter a different code and press `#` to increment the failed-attempt count. After three wrong checks, `uo_out[1]` should go high.

The included Cocotb testbench models the external keypad matrix and verifies reset, row scanning, `uio_oe`, password storage with `*`, password checking with `#`, the `unlocked` output, and `locked_out` after three wrong attempts.

## External hardware

A 4x4 matrix keypad is required for hardware testing. Optional LEDs or logic analyzer probes can be connected to the output pins to observe `unlocked`, `locked_out`, failed attempts, and password/debug bits.
