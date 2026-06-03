# Verification

Run the TinyTapeout Cocotb testbench from the repository root:

```sh
make -C test
```

The RTL testbench instantiates `tt_um_combolock` without a parameter override, matching the synthesized gate-level netlist. The Cocotb test waits for the default `LOCKOUT_CYCLES=1024` timeout through the external decimal-point lockout indicator.

The Cocotb test covers:

- Reset behavior and fixed `uio_oe = 8'b0000_1111`
- Keypad row scanning and key mapping
- Password storage using `*`
- Password verification using `#`
- 7-segment output patterns on `uo_out[6:0]`
- Decimal-point lockout indication on `uo_out[7]`
- Three failed attempts entering temporary lockout
- Ignored keypad updates during temporary lockout
- Lockout timeout clearing the decimal-point indicator
- Successful password check after the timeout
- Reset while locked out
