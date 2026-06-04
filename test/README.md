# Cocotb Testbench

This testbench uses [cocotb](https://docs.cocotb.org/en/stable/) to verify `tt_um_combolock` with the active RTL source list in [Makefile](Makefile).

## What it covers

- Reset behavior and fixed `uio_oe = 8'b0000_1111`
- 4x4 keypad row scanning and key mapping
- Password storage with `*` and password checking with `#`
- Active-high 7-segment output patterns on `uo_out[6:0]`
- Decimal-point lockout indication on `uo_out[7]`
- Temporary lockout after three wrong attempts, ignored inputs during lockout, timeout recovery, and reset while locked out

## How to run

From the repository root:

```sh
make -C test
```

From this directory:

```sh
make
```

To run a gate-level simulation, copy a generated `tt_um_combolock` gate-level netlist to `gate_level_netlist.v` and run:

```sh
make GATES=yes
```

The RTL testbench writes `tb.fst` by default.

## How to view the waveform file

```sh
gtkwave tb.fst tb.gtkw
surfer tb.fst
```
