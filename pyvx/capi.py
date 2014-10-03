from codegen import PythonApi, export
from pyvx import *


class OpenVxApi(PythonApi):
    cdef = """
        typedef long vx_context;
    """

    @export("vx_context()")
    def vxCreateContext(self):
        return self.store(Context())

if __name__ == '__main__':
    import sys
    api = OpenVxApi(True)
    api.build(sys.argv[1])
