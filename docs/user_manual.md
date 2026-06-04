# User Manual

## Basic operation

Connect a standard 4x4 matrix keypad to `uio[7:0]`. The ASIC drives keypad rows on `uio[3:0]` and reads keypad columns on `uio[7:4]`.

When the design is not locked out, keys `0` through `9` and `A` through `D` select the current 4-bit code. Press `*` to store the current code as the password. Press `#` to check the current code against the stored password.

Active-low reset clears the password to 0, clears the entered code, resets the failed-attempt counter, clears the internal unlocked state, and exits any temporary lockout.

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

The internal lockout timer counts down for a fixed number of clock cycles. When the timer expires, `locked_out` clears, the failed-attempt count returns to 0, and `unlocked` remains 0. The user can then enter the password and press `#` again.

The stored password remains in volatile flip-flops during temporary lockout. Reset immediately clears `locked_out`, failed attempts, `unlocked`, the internal lockout timer, and the password register. Future work could add EEPROM or FRAM storage if the password must survive reset or power loss.
