"""
:mod:`pyvx`
==========================================
"""

__version_info__ = (0, 3, 0)
__version__ = '.'.join(str(i) for i in __version_info__)
__backend_version__ = b'1.0.1-2'

_default_backend_name = '_default'

import sys
if sys.version_info > (3,):
    from importlib import reload


def use_backend(backend):
    """
    Specifies which backend to use. It is typically called before any other
    modules are imported. If it is called later it will reload the modules.
    However if any symbols was imported from the modules, they will have to
    be reimported. If it is not called, the default backend will be used.

    The *backend* parameter can either be an already imported module or a
    string which specifyes a module under *pyvx.backend* to load. That is the
    same string that was passed as the *name* argument of build_cbackend during
    `installation`_. The first form allows for backends that's not part of
    pyvx to be used.

    .. _`installation`: #installation

    Typical usage:

    .. code-block:: python

        from pyvx import use_backend
        use_backend("sample")
        from pyvx import vx
    """
    """
    :param backend:
    :return:
    """
    import pyvx
    pyvx._default_backend_name = backend
    for n in ['backend', '_auto_vx', '_auto_vxu', 'types', 'vx', 'vxu', 'pythonic']:
        n = 'pyvx.' + n
        if n in sys.modules:
            reload(sys.modules[n])