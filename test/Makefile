all: python_test c_test

python_test:
	cd .. && py.test -v -s

c_test:
	-rm -rf ../pyvx/__pycache__
	cd .. && python -mpyvx.capi build build
	./checkmk *.ts > tests.c
	gcc tests.c -g -I../build/include -L../build/lib -Wl,-rpath,`pwd`/../build/lib/ -lopenvx -lcheck -lpthread -lm -lrt
	PYTHONPATH=.. ./a.out

