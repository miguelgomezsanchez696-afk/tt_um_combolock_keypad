# User Manual

## Basic operation

Connect a standard 4x4 matrix keypad to `uio[7:0]`. The ASIC drives keypad rows on `uio[3:0]` and reads keypad columns on `uio[7:4]`.

When the design is not locked out, keys `0` through `9` and `A` through `D` select the current 4-bit code. Press `*` to store the current code as the password. Press `#` to check the current code against the stored password.

## Status outputs

`uo_out[6:0]` drives an active-high 7-segment display for the current entered hex digit. The bit order is `uo_out[0] = a`, `uo_out[1] = b`, `uo_out[2] = c`, `uo_out[3] = d`, `uo_out[4] = e`, `uo_out[5] = f`, and `uo_out[6] = g`. `uo_out[7]` drives the decimal point and is high during temporary lockout.

| Hex | `uo_out[6:0]` |
|---|---|
| 0 | `0x3f` |
| 1 | `0x06` |
| 2 | `0x5b` |
| 3 | `0x4f` |
| 4 | `0x66` |
| 5 | `0x6d` |
| 6 | `0x7d` |
| 7 | `0x07` |
| 8 | `0x7f` |
| 9 | `0x6f` |
| A | `0x77` |
| B | `0x7c` |
| C | `0x39` |
| D | `0x5e` |
| E | `0x79` |
| F | `0x71` |

## Temporary lockout

After three wrong password checks, `locked_out` asserts. During this temporary lockout state, code-entry keys, password checks with `#`, and password changes with `*` are ignored.

The user must wait until the internal lockout timer expires or reset the chip with `rst_n`. When the timer expires, `locked_out` clears, the failed-attempt count returns to 0, and `unlocked` remains 0. The user can then enter the password and press `#` again.

Reset immediately clears `locked_out`, failed attempts, `unlocked`, and the internal lockout timer.
