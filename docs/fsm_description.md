# FSM-Like Behavior

The RTL is implemented as registered lock logic rather than a separately encoded FSM, but its behavior can be described with the following states.

## IDLE

The design is locked, not in lockout, and waiting for keypad input. Reset returns the design to this behavior with password, entered code, attempts, unlock, lockout, and timer state cleared.

## CODE_ENTRY

Keys `0` through `9` and `A` through `D` load the current 4-bit code while the design is not locked out.

## PASSWORD_SET

Pressing `*` stores the current code as the password when the design is not locked out. This clears failed attempts and clears `unlocked`.

## CHECK_CODE

Pressing `#` compares the current code with the stored password when the design is not locked out.

## UNLOCKED

If the current code matches the stored password, `unlocked` asserts and failed attempts reset to 0. A later wrong check clears `unlocked`.

## FAILED_ATTEMPT

If the current code does not match the stored password, `unlocked` clears and the failed-attempt counter increments. Failed attempts 1 and 2 return to normal code entry. Failed attempt 3 enters temporary lockout.

## TEMP_LOCKOUT

After the third wrong check, `locked_out` asserts, failed attempts report 3, and the internal lockout timer loads `LOCKOUT_CYCLES`. While this state is active, code-entry keys, `*`, and `#` are ignored, `unlocked` stays 0, and failed attempts do not keep incrementing.

When the timer expires, `locked_out` clears, failed attempts reset to 0, and `unlocked` remains 0. The design then returns to normal code entry. Reset exits this state immediately and clears the timer.
