from pyvx.pythonic import *

class TestPythonic(object):
    def test_context(self):
        with Context() as c:
            assert c.type == c.vx.TYPE_CONTEXT
