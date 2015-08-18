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

    def test_create_image(self):
        c = CreateContext()
        img = CreateImage(c, 640, 480, DF_IMAGE_UYVY)
        assert img is not None
        img = CreateImage(c, -100, -100, DF_IMAGE_UYVY)
        assert img is None
