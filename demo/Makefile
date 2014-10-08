all: simple 

%: %.c
	cd .. && python -mpyvx.capi build openvx
	gcc -o $@ $^ -g -L.. -lopenvx

run-%: %
	LD_LIBRARY_PATH=.. ./$^
