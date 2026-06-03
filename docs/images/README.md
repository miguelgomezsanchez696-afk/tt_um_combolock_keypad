# Visual Evidence Images

The PNG files in this directory are documentation evidence for the ASIC project.

Generated documentation images:

- `block_diagram.png`
- `keypad_mapping.png`
- `signoff_summary.png`

Captured tool screenshots:

- `rtl_waveform_capture.png` is a GTKWave waveform screenshot from the RTL simulation VCD.
- `klayout_view.png` is a KLayout screenshot of the final layout.
- `tinytapeout_3d_view.png` is a TinyTapeout GDS Viewer 3D screenshot of the final layout.

To regenerate the simulation waveform locally:

```sh
make sim
gtkwave sim/tb_combolock.vcd
```

Recommended waveform signals:

- `clk`
- `rst_n`
- `uio_in`
- `uio_out`
- `uio_oe`
- `uo_out`
- `tb_combolock.dut.key_valid`
- `tb_combolock.dut.key_code`
- `tb_combolock.dut.key_star`
- `tb_combolock.dut.key_hash`
- `tb_combolock.dut.unlocked`
- `tb_combolock.dut.locked_out`
- `tb_combolock.dut.attempts`

To inspect the committed final layout manually, open:

```sh
klayout docs/gds/tt_um_combolock.gds
```

The complete signoff run was local. Extracted evidence is committed under `reports/`, and the final GDS viewer file is committed under `docs/gds/tt_um_combolock.gds`.
