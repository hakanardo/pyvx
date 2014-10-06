test:
	python -mpyvx.capi build openvx
	gcc test.c  -L. -lopenvx
	LD_LIBRARY_PATH=. ./a.out