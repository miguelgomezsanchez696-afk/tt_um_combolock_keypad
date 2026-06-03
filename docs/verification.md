# Verification

Run the TinyTapeout Cocotb testbench from the repository root:

```sh
make -C test
```

The RTL testbench instantiates `tt_um_combolock` with `LOCKOUT_CYCLES=8` so the temporary lockout timer can be verified quickly in simulation. The synthesized default remains `LOCKOUT_CYCLES=1024`.

The Cocotb test covers:

- Reset behavior and fixed `uio_oe = 8'b0000_1111`
- Keypad row scanning and key mapping
- Password storage using `*`
- Password verification using `#`
- Correct-password unlock behavior
- Three failed attempts entering temporary lockout
- Ignored password changes during temporary lockout
- Ignored password checks during temporary lockout
- Stable failed-attempt count while locked out
- Lockout timeout clearing `locked_out` and resetting failed attempts
- Successful unlock after the timeout
- Reset while locked out
