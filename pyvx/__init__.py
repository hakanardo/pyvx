__version_info__ = (0, 3, 0)
__version__ = '.'.join(str(i) for i in __version_info__)
__backend_version__ = '1.0.1-1'

import sys
class ImportVX(object):

    def find_module(self, fullname, path=None):
        if fullname == 'pyvx.vx':
            return self
        return None

    def load_module(self, name):
        from pyvx.default import vx
        return vx

import sys
sys.meta_path = [ImportVX()]
