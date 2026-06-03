.PHONY: sim cocotb test clean

sim:
	$(MAKE) -C test

cocotb:
	$(MAKE) -C test

test:
	$(MAKE) -C test

clean:
	$(MAKE) -C test clean || true
	rm -f test/*.vcd test/*.fst test/*.xml test/results.xml

