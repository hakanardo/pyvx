test:
	python -mpyvx.capi openvx
	gcc test.c  -L. -lopenvx
	LD_LIBRARY_PATH=. ./a.out