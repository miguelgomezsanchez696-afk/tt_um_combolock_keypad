![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# 4-bit Combination Lock with 4x4 Matrix Keypad

- [Read the project documentation](docs/info.md)

## What is Tiny Tapeout?

Tiny Tapeout is an educational project that makes it easier and cheaper to manufacture small digital and analog designs on a real chip.

To learn more and get started, visit <https://tinytapeout.com>.

## Project overview

This project implements a TinyTapeout 4-bit combination lock using a standard 4x4 matrix keypad instead of DIP switches. The top module is `tt_um_combolock`, with keypad scanning in `src/keypad_scanner.v` and lock/status logic in `src/tt_um_combolock.v`.

Behavior summary:

- Keys `0`-`9` and `A`-`D` load the current 4-bit code when the lock is not in lockout.
- `*` stores the current code as the password when the lock is not in lockout.
- `#` checks the current code against the stored password when the lock is not in lockout.
- After three failed attempts, the lock enters a temporary lockout state. When the internal timer expires, attempts reset and the user can try again.

Detailed design, pinout, test, and hardware instructions are in [docs/info.md](docs/info.md).

## Quick test

Run the Cocotb testbench from the repository root:

```sh
make -C test
```

## Evidence and layout

- [Visual evidence](docs/images/)
- [Final GDS](docs/gds/tt_um_combolock.gds)
- [Physical verification reports](reports/)
