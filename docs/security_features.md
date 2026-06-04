# Security Features

## Password register

The design stores one 4-bit password in an internal flip-flop register. The stored password is not exposed directly on `uo_out`; the outputs drive a 7-segment display for the current entered code plus a decimal-point lockout indicator.

## Keypad entry

A 4x4 matrix keypad provides the user input. Keys `0` through `9` and `A` through `D` load the current 4-bit code when the design is not locked out. The `*` key stores the current code as the password when the design is not locked out. The `#` key checks the current code when the design is not locked out.

## Three-attempt policy

Each wrong `#` check increments the failed-attempt counter. After the third wrong check, the counter reaches 3 and `locked_out` asserts.

## Temporary lockout timer

Lockout is temporary. While `locked_out` is active, code entry, password checks, and password changes are ignored, `unlocked` is held low, and failed attempts do not keep incrementing. The stored password remains in volatile flip-flops during this temporary lockout. An internal lockout timer counts down for a fixed number of clock cycles. When the timer expires, `locked_out` clears and failed attempts reset to 0.

The default RTL parameter is `LOCKOUT_CYCLES=1024`. The Cocotb testbench uses the synthesized default instead of an RTL-only parameter override so RTL and gate-level simulations exercise the same timeout.

## Reset behavior

Active-low reset clears the password, entered code, failed attempts, `unlocked`, `locked_out`, and the internal lockout timer immediately.

## Limitations

The password is volatile because it is stored in flip-flops. It is lost on reset or power loss.

## Future improvement

A future version could store the password in external EEPROM or FRAM so the programmed password survives reset and power loss.
