all: simple view

%: %.c
	-rm -rf ../pyvx/__pycache__
	-ln -s ../pyvx .
	cd .. && python -mpyvx.capi build build
	gcc -o $@ $^ -g -I../build/include -L../build/lib -Wl,-rpath,`pwd`/../build/lib/ -lopenvx

