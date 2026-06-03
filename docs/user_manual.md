# User Manual

## Basic operation

Connect a standard 4x4 matrix keypad to `uio[7:0]`. The ASIC drives keypad rows on `uio[3:0]` and reads keypad columns on `uio[7:4]`.

When the design is not locked out, keys `0` through `9` and `A` through `D` select the current 4-bit code. Press `*` to store the current code as the password. Press `#` to check the current code against the stored password.

## Status outputs

| Output bit | Meaning |
|---|---|
| `uo_out[0]` | `unlocked` |
| `uo_out[1]` | `locked_out` |
| `uo_out[3:2]` | failed-attempt count |
| `uo_out[7:4]` | stored password/debug bits |

## Temporary lockout

After three wrong password checks, `locked_out` asserts. During this temporary lockout state, code-entry keys, password checks with `#`, and password changes with `*` are ignored.

The user must wait until the internal lockout timer expires or reset the chip with `rst_n`. When the timer expires, `locked_out` clears, the failed-attempt count returns to 0, and `unlocked` remains 0. The user can then enter the password and press `#` again.

Reset immediately clears `locked_out`, failed attempts, `unlocked`, and the internal lockout timer.
