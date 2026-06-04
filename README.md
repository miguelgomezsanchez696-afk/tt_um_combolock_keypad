![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# 4-bit Combination Lock with 4x4 Matrix Keypad

## Project overview

This project implements a TinyTapeout 4-bit combination lock using a standard 4x4 matrix keypad instead of DIP switches. It is based on the official TinyTapeout `ttsky-verilog-template` structure and is prepared for the usual `docs`, `test`, `gds`, and viewer-oriented checks.

The top module is `tt_um_combolock`. Keypad scanning is implemented in `src/keypad_scanner.v`, lock control is implemented in `src/tt_um_combolock.v`, and the active-high 7-segment output is implemented in `src/seven_seg_decoder.v`.

## Main features

- Keys `0`-`9` and `A`-`D` load the current 4-bit code when the lock is not in lockout.
- `*` stores the current code as the password when the lock is not in lockout.
- `#` checks the current code against the stored password when the lock is not in lockout.
- After three failed attempts, a temporary lockout starts. Unlock attempts are ignored while the internal timer counts down.
- When the timer expires, lockout clears, failed attempts reset, and the user can try again. Reset clears lockout immediately.
- During lockout, the password remains stored in volatile flip-flops; reset or power loss clears it. Future work could add EEPROM or FRAM storage.
- `uo_out[6:0]` drives the current entered hex digit on a 7-segment display, and `uo_out[7]` drives the decimal point as the lockout indicator.

Detailed design, pinout, test, and hardware instructions are kept in the project documentation.

## Quick test

Run the Cocotb testbench from the repository root:

```sh
make -C test
```

## Evidence and layout

- [Required TinyTapeout project info](docs/info.md)
- [User manual](docs/user_manual.md)
- [Verification notes](docs/verification.md)
- [Security features](docs/security_features.md)
- [FSM-like behavior](docs/fsm_description.md)
- [Project review checklist](docs/project_review_checklist.md)
- [Visual evidence images](docs/images/)
- [Final GDS visual evidence](docs/gds/)
- [Physical verification reports](reports/)

The complete physical evidence from the local signoff run is in `reports/`. Final GDS visual evidence is in `docs/gds/`.
