from pyvx.backend.mock_backend import Lib, ffi

class Lib2(Lib):
    def vxCreateContext(self):
        return 7

lib = Lib2()
