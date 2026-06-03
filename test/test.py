# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge


UNPRESSED_UIO_IN = 0xF0
ROW_PATTERNS = [0b1110, 0b1101, 0b1011, 0b0111]
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


def output_fields(dut):
    value = int(dut.uo_out.value)
    return {
        "unlocked": value & 0x1,
        "locked_out": (value >> 1) & 0x1,
        "attempts": (value >> 2) & 0x3,
        "password": (value >> 4) & 0xF,
    }


def current_scan_row(dut):
    rows = int(dut.uio_out.value) & 0xF
    for row, pattern in enumerate(ROW_PATTERNS):
        if rows == pattern:
            return row
    return None


async def wait_for_scan_row(dut, row):
    expected = ROW_PATTERNS[row]
    for _ in range(12):
        await FallingEdge(dut.clk)
        if (int(dut.uio_out.value) & 0xF) == expected:
            return
    raise AssertionError(f"row scan never reached row {row}")


async def release_key(dut, cycles=8):
    dut.uio_in.value = UNPRESSED_UIO_IN
    await ClockCycles(dut.clk, cycles)


async def press_key(dut, key):
    row, col, _ = KEYS[key]
    saw_selected_row = False

    for _ in range(8):
        await FallingEdge(dut.clk)
        cols = 0xF
        if current_scan_row(dut) == row:
            cols &= ~(1 << col)
            saw_selected_row = True
        dut.uio_in.value = cols << 4

    assert saw_selected_row, f"key {key} was never presented on its selected row"
    await release_key(dut)


async def store_password(dut, key):
    await press_key(dut, key)
    await press_key(dut, "*")
    expected = KEYS[key][2]
    fields = output_fields(dut)
    assert fields["password"] == expected, f"stored password for {key} was {fields['password']:x}"
    assert fields["attempts"] == 0
    assert fields["unlocked"] == 0
    assert fields["locked_out"] == 0


@cocotb.test()
async def test_combination_lock_keypad(dut):
    dut.clk.value = 0
    try:
        clock = Clock(dut.clk, 25, unit="ns")
    except TypeError:
        clock = Clock(dut.clk, 25, units="ns")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = UNPRESSED_UIO_IN
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 4)
    assert int(dut.uo_out.value) == 0
    assert int(dut.uio_oe.value) == 0x0F
    assert (int(dut.uio_out.value) & 0xF) == ROW_PATTERNS[0]

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert output_fields(dut) == {
        "unlocked": 0,
        "locked_out": 0,
        "attempts": 0,
        "password": 0,
    }

    await wait_for_scan_row(dut, 0)
    observed_rows = [int(dut.uio_out.value) & 0xF]
    for _ in range(3):
        await FallingEdge(dut.clk)
        observed_rows.append(int(dut.uio_out.value) & 0xF)
    assert observed_rows == ROW_PATTERNS
    assert int(dut.uio_oe.value) == 0x0F

    for key in CODE_KEYS:
        await store_password(dut, key)

    await store_password(dut, "5")
    await press_key(dut, "5")
    await press_key(dut, "#")
    fields = output_fields(dut)
    assert fields["password"] == 0x5
    assert fields["attempts"] == 0
    assert fields["unlocked"] == 1
    assert fields["locked_out"] == 0

    for attempt, key in enumerate(["1", "2", "3"], start=1):
        await press_key(dut, key)
        await press_key(dut, "#")
        fields = output_fields(dut)
        assert fields["password"] == 0x5
        assert fields["attempts"] == attempt
        assert fields["unlocked"] == 0
        assert fields["locked_out"] == (1 if attempt == 3 else 0)

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    assert output_fields(dut) == {
        "unlocked": 0,
        "locked_out": 0,
        "attempts": 0,
        "password": 0,
    }
