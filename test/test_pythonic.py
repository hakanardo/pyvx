from pyvx.pythonic import *

class TestPythonic(object):
    def test_context(self):
        with Context() as c:
            assert c.type == vx.TYPE_CONTEXT
            vid = c.vendor_id
