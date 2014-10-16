all: simple view

%: %.c
	-rm -rf ../pyvx/__pycache__
	cd .. && python -mpyvx.capi build
	gcc -o $@ $^ -g -I.. -L.. -lopenvx

run-%: %
	LD_LIBRARY_PATH=.. ./$^
