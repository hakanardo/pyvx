all: simple 

%: %.c
	-rm -r ../pyvx/__pycache__
	cd .. && python -mpyvx.capi build openvx
	gcc -o $@ $^ -g -I.. -L.. -lopenvx

run-%: %
	LD_LIBRARY_PATH=.. ./$^
