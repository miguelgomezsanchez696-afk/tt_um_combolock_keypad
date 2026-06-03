# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge


LOCKOUT_CYCLES = 1024
LOCKOUT_MARGIN_CYCLES = 64
UNPRESSED_UIO_IN = 0xF0
ROW_PATTERNS = [0b1110, 0b1101, 0b1011, 0b0111]
SEVEN_SEG = {
    0x0: 0x3F,
    0x1: 0x06,
    0x2: 0x5B,
    0x3: 0x4F,
    0x4: 0x66,
    0x5: 0x6D,
    0x6: 0x7D,
    0x7: 0x07,
    0x8: 0x7F,
    0x9: 0x6F,
    0xA: 0x77,
    0xB: 0x7C,
    0xC: 0x39,
    0xD: 0x5E,
    0xE: 0x79,
    0xF: 0x71,
}
KEYS = {
    "1": (0, 0, 0x1),
    "2": (0, 1, 0x2),
    "3": (0, 2, 0x3),
    "A": (0, 3, 0xA),
    "4": (1, 0, 0x4),
    "5": (1, 1, 0x5),
    "6": (1, 2, 0x6),
    "B": (1, 3, 0xB),
    "7": (2, 0, 0x7),
    "8": (2, 1, 0x8),
    "9": (2, 2, 0x9),
    "C": (2, 3, 0xC),
    "*": (3, 0, 0xE),
    "0": (3, 1, 0x0),
    "#": (3, 2, 0xF),
    "D": (3, 3, 0xD),
}
CODE_KEYS = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "0", "D"]


def signal_int(signal):
    try:
        return int(signal.value)
    except ValueError:
        return None


def display_value(digit, locked_out=False):
    return SEVEN_SEG[digit] | (0x80 if locked_out else 0x00)


def format_value(value):
    return "X" if value is None else f"0x{value:02x}"


def current_scan_row(dut):
    value = signal_int(dut.uio_out)
    if value is None:
        return None

    rows = value & 0xF
    for row, pattern in enumerate(ROW_PATTERNS):
        if rows == pattern:
            return row
    return None


async def wait_for_uo(dut, expected, timeout_cycles=64, stable_cycles=2):
    stable_seen = 0
    last_value = None

    for _ in range(timeout_cycles):
        await ClockCycles(dut.clk, 1)
        last_value = signal_int(dut.uo_out)
        if last_value == expected:
            stable_seen += 1
            if stable_seen >= stable_cycles:
                return
        else:
            stable_seen = 0

    raise AssertionError(
        f"uo_out did not settle to 0x{expected:02x}; last value was {format_value(last_value)}"
    )


async def expect_display(dut, digit, locked_out=False, timeout_cycles=64):
    await wait_for_uo(dut, display_value(digit, locked_out), timeout_cycles=timeout_cycles)


async def wait_for_uio_oe(dut, expected=0x0F, timeout_cycles=32):
    last_value = None
    for _ in range(timeout_cycles):
        await ClockCycles(dut.clk, 1)
        last_value = signal_int(dut.uio_oe)
        if last_value == expected:
            return

    raise AssertionError(
        f"uio_oe did not settle to 0x{expected:02x}; last value was {format_value(last_value)}"
    )


async def wait_for_lockout_state(dut, locked_out, timeout_cycles):
    expected = 0x80 if locked_out else 0x00
    last_value = None

    for _ in range(timeout_cycles):
        last_value = signal_int(dut.uo_out)
        if last_value is not None and (last_value & 0x80) == expected:
            return
        await ClockCycles(dut.clk, 1)

    state = "assert" if locked_out else "clear"
    raise AssertionError(
        f"lockout decimal point did not {state}; last uo_out was {format_value(last_value)}"
    )


async def wait_for_scan_row(dut, row, timeout_cycles=32):
    expected = ROW_PATTERNS[row]
    last_rows = None

    for _ in range(timeout_cycles):
        await FallingEdge(dut.clk)
        value = signal_int(dut.uio_out)
        if value is None:
            last_rows = None
            continue

        last_rows = value & 0xF
        if last_rows == expected:
            return

    raise AssertionError(
        f"row scan never reached row {row}; last rows were {format_value(last_rows)}"
    )


async def release_key(dut, cycles=12):
    dut.uio_in.value = UNPRESSED_UIO_IN
    await ClockCycles(dut.clk, cycles)


async def press_key(dut, key, hold_cycles=24):
    row, col, _ = KEYS[key]
    saw_selected_row = False

    for _ in range(hold_cycles):
        await FallingEdge(dut.clk)

        cols = 0xF
        if current_scan_row(dut) == row:
            cols &= ~(1 << col)
            saw_selected_row = True

        dut.uio_in.value = cols << 4

    assert saw_selected_row, f"key {key} was never presented on its selected row"
    await release_key(dut)


async def reset_design(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = UNPRESSED_UIO_IN
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 8)
    await expect_display(dut, 0, locked_out=False)
    await wait_for_uio_oe(dut)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 8)
    await expect_display(dut, 0, locked_out=False)
    await wait_for_uio_oe(dut)


async def store_password(dut, key):
    digit = KEYS[key][2]
    await press_key(dut, key)
    await expect_display(dut, digit, locked_out=False)
    await press_key(dut, "*")
    await expect_display(dut, digit, locked_out=False)


async def wrong_attempt(dut, key, expect_lockout=False):
    digit = KEYS[key][2]
    await press_key(dut, key)
    await expect_display(dut, digit, locked_out=False)
    await press_key(dut, "#")

    if expect_lockout:
        await wait_for_lockout_state(dut, True, timeout_cycles=96)
        await expect_display(dut, digit, locked_out=True)
    else:
        await wait_for_lockout_state(dut, False, timeout_cycles=24)
        await expect_display(dut, digit, locked_out=False)


@cocotb.test()
async def test_combination_lock_keypad(dut):
    dut.clk.value = 0
    try:
        clock = Clock(dut.clk, 25, unit="ns")
    except TypeError:
        clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    await reset_design(dut)

    await wait_for_scan_row(dut, 0)
    observed_rows = []
    for _ in range(4):
        value = signal_int(dut.uio_out)
        assert value is not None, "uio_out was unknown while checking row scan"
        observed_rows.append(value & 0xF)
        await FallingEdge(dut.clk)
    assert observed_rows == ROW_PATTERNS

    for key in CODE_KEYS:
        await store_password(dut, key)

    await store_password(dut, "5")

    await press_key(dut, "5")
    await expect_display(dut, 0x5, locked_out=False)
    await press_key(dut, "#")
    await expect_display(dut, 0x5, locked_out=False)

    await wrong_attempt(dut, "1", expect_lockout=False)
    await wrong_attempt(dut, "2", expect_lockout=False)
    await wrong_attempt(dut, "3", expect_lockout=True)

    for ignored_key in ["A", "*", "5", "#"]:
        await press_key(dut, ignored_key)
        await expect_display(dut, 0x3, locked_out=True)

    await wait_for_lockout_state(
        dut, False, timeout_cycles=LOCKOUT_CYCLES + LOCKOUT_MARGIN_CYCLES
    )
    await expect_display(dut, 0x3, locked_out=False)

    await press_key(dut, "5")
    await expect_display(dut, 0x5, locked_out=False)
    await press_key(dut, "#")
    await expect_display(dut, 0x5, locked_out=False)

    await wrong_attempt(dut, "1", expect_lockout=False)
    await wrong_attempt(dut, "2", expect_lockout=False)
    await wrong_attempt(dut, "3", expect_lockout=True)

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    await expect_display(dut, 0x0, locked_out=False)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 8)
    await expect_display(dut, 0x0, locked_out=False)
