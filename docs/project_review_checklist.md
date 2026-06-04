# Project Review Checklist

- [x] Top module remains `tt_um_combolock`
- [x] TinyTapeout interface and pinout unchanged
- [x] `uio_oe` remains `8'b0000_1111`
- [x] RTL source list includes `tt_um_combolock.v`, `keypad_scanner.v`, and `seven_seg_decoder.v`
- [x] Temporary lockout timer implemented
- [x] Temporary lockout verified in Cocotb
- [x] Temporary lockout ignores keypad updates while the timer counts down
- [x] Lockout timeout clears lockout and resets failed attempts
- [x] Reset clears lockout immediately
- [x] Password storage documented as volatile flip-flops, with EEPROM/FRAM as future work
- [x] Documentation updated for temporary lockout behavior
- [x] Documentation updated without stale lockout wording
