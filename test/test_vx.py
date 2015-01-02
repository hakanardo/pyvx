from pyvx.vx import *

class TestVx(object):
    def test_veresion(self):
        c = CreateContext()
        status, version = QueryContext(c, CONTEXT_ATTRIBUTE_VERSION)
        assert(status == SUCCESS)
        assert(version == VERSION)
        status, name = QueryContext(c, KERNEL_ATTRIBUTE_NAME)
        assert(status != SUCCESS)
        ReleaseContext(c)
