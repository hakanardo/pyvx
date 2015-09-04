__version_info__ = (0, 3, 0)
__version__ = '.'.join(str(i) for i in __version_info__)
__backend_version__ = '1.0.1-2'

_default_backend_name = '_default'

def use_backend(backend):
    import pyvx, sys
    pyvx._default_backend_name = backend
    for n in ['backend', '_auto_vx', '_auto_vxu', 'types', 'vx', 'vxu', 'pythonic']:
        n = 'pyvx.' + n
        if n in sys.modules:
            reload(sys.modules[n])