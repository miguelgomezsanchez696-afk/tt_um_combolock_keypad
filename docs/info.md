## How it works

This project implements a 4-bit digital combination lock using a 4x4 matrix keypad as the user input interface.

The design is based on a TinyTapeout-style Combination Lock. The main functional modification is that the password is no longer entered using DIP switches. Instead, a standard 4x4 matrix keypad is scanned through the bidirectional uio pins.

The ASIC drives the keypad rows through uio_out[3:0] and reads the keypad columns through uio_in[7:4]. The output enable value is fixed as uio_oe = 8'b0000_1111, so uio[3:0] are outputs and uio[7:4] are inputs.

Keypad layout:

Row 0: 1, 2, 3, A
Row 1: 4, 5, 6, B
Row 2: 7, 8, 9, C
Row 3: *, 0, #, D

Keys 0 to 9 and A to D load the current 4-bit entered code. The * key stores the current entered code as the password. The # key checks the entered code against the stored password.

If the entered code matches the stored password, uo_out[0] is asserted as the unlocked output. If the entered code is incorrect, the failed-attempt counter increases. After three failed attempts, uo_out[1] is asserted as locked_out.

## How to test

Run the TinyTapeout Cocotb testbench from the repository root with:

    make -C test

The testbench verifies:

- Reset behavior
- Keypad row scanning
- uio_oe = 8'b0000_1111
- Password entry using keypad keys
- Password storage using *
- Password verification using #
- Unlock behavior with the correct password
- Lockout behavior after three failed attempts

Expected result:

    PASS

## External hardware

This design is intended to be used with a standard 4x4 matrix keypad.

Keypad connections:

| Keypad signal | ASIC signal |
|---|---|
| Row 0 | uio[0] |
| Row 1 | uio[1] |
| Row 2 | uio[2] |
| Row 3 | uio[3] |
| Column 0 | uio[4] |
| Column 1 | uio[5] |
| Column 2 | uio[6] |
| Column 3 | uio[7] |

The dedicated ui_in[7:0] inputs are unused in this version.
