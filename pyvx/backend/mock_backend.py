import pyvx

class Lib(object):
    def vxCreateContext(self):
        return 42

    def __getattr__(self, item):
        return -1

    def _get_backend_version(self):
        return pyvx.__backend_version__

    def _get_backend_name(self):
        return "mock"

    def _get_backend_install_path(self):
        return "nowhere"

    def _get_FMT_REF(self):
        return ""

    def _get_FMT_SIZE(self):
        return ""

class Ffi(object):
    def string(self, obj):
        return str(obj)

    def typeof(self, obj):
        return None

lib, ffi = Lib(), Ffi()