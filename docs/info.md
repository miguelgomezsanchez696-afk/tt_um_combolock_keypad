## How it works

### 4-bit combination lock with keypad input

This project implements a 4-bit combination lock for TinyTapeout. It is based on a simple Combination Lock design, with the main modification that password entry uses a standard 4x4 matrix keypad instead of DIP switches.

The design is organized into three functional blocks:

- `keypad_scanner`: scans the keypad matrix by driving one row at a time on `uio_out[3:0]` and reading the column inputs on `uio_in[7:4]`.
- Lock logic: stores the current 4-bit password, accepts keypad code entries, checks the entered code, and counts failed attempts.
- Output/status register: reports unlock, lockout, failed-attempt count, and password/debug bits on `uo_out[7:0]`.

![Block diagram](images/block_diagram.png)

The keypad rows are active-low scan outputs. The columns are active-low inputs, so an unpressed keypad presents all column inputs high. The bidirectional output enable is fixed to `uio_oe = 8'b0000_1111`, making `uio[3:0]` outputs and `uio[7:4]` inputs.

![Keypad mapping](images/keypad_mapping.png)

### Keypad mapping

| Row | Column 0 | Column 1 | Column 2 | Column 3 |
|---|---|---|---|---|
| Row 0 | 1 | 2 | 3 | A |
| Row 1 | 4 | 5 | 6 | B |
| Row 2 | 7 | 8 | 9 | C |
| Row 3 | * | 0 | # | D |

Keys `0` through `9` and `A` through `D` load the current 4-bit code. The `*` key stores the current code as the password. The `#` key checks the current code against the stored password.

When the entered code matches the stored password, `uo_out[0]` is asserted as `unlocked`. A wrong code increments the failed-attempt counter on `uo_out[3:2]`. After three wrong attempts, `uo_out[1]` is asserted as `locked_out`.

The status output format is:

| Output bits | Function |
|---|---|
| `uo_out[0]` | `unlocked` |
| `uo_out[1]` | `locked_out` |
| `uo_out[3:2]` | failed-attempt count |
| `uo_out[7:4]` | stored password/debug bits |

### Pinout interface

The following table summarizes the TinyTapeout interface used by this design.

| TinyTapeout signal | Direction | Function |
|---|---|---|
| `clk` | input | System clock for keypad scanning and lock logic |
| `rst_n` | input | Active-low reset; clears password, entered code, attempts, unlock, and lockout state |
| `ena` | input | Design enable; lock state updates when asserted |
| `ui[7:0]` | input | Unused/reserved in this version |
| `uo[7:0]` | output | Lock status: `unlocked`, `locked_out`, failed attempts, and password/debug bits |
| `uio[7:0]` | bidirectional | 4x4 keypad interface: rows on `uio[3:0]`, columns on `uio[7:4]` |

## How to test

Run the TinyTapeout Cocotb testbench from the repository root:

```sh
make -C test
```

Expected result:

```text
PASS
```

The Cocotb test verifies:

- Reset behavior
- Keypad row scanning
- `uio_oe = 8'b0000_1111`
- Password storage using `*`
- Password checking using `#`
- Unlock behavior with the correct password
- Lockout behavior after three wrong attempts

Optional local visual inspection:

- Open [docs/gds/tt_um_combolock.gds](gds/tt_um_combolock.gds) in the TinyTapeout GDS Viewer.
- Check [docs/images/rtl_waveform_capture.png](images/rtl_waveform_capture.png) for RTL simulation waveform evidence.
- Check [docs/images/klayout_view.png](images/klayout_view.png) for final layout inspection.
- Check [docs/images/tinytapeout_3d_view.png](images/tinytapeout_3d_view.png) for the TinyTapeout 3D layout view.

Physical verification and manufacturability evidence is kept in [reports/](../reports/), including DRC, LVS, antenna, final metrics, and manufacturability reports.

## External hardware

This design is intended to be used with a standard 4x4 matrix keypad. The ASIC drives the row lines and reads the column lines through the TinyTapeout bidirectional `uio` pins.

| Keypad signal | TinyTapeout signal |
|---|---|
| Row 0 | `uio[0]` |
| Row 1 | `uio[1]` |
| Row 2 | `uio[2]` |
| Row 3 | `uio[3]` |
| Column 0 | `uio[4]` |
| Column 1 | `uio[5]` |
| Column 2 | `uio[6]` |
| Column 3 | `uio[7]` |

The dedicated `ui_in[7:0]` inputs are unused/reserved in this version.
