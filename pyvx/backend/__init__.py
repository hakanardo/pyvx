import pyvx

if isinstance(pyvx._default_backend_name, str):
    try:
        exec("from pyvx.backend.%s import lib, ffi" % pyvx._default_backend_name)
    except ImportError:
        raise ImportError("No default backend found. Please build one using:\n\n" +
                          "    python -mpyvx.build_cbackend --default name /path/to/openvx/install\n" +
                          "")
else:
    lib = pyvx._default_backend_name.lib
    ffi = pyvx._default_backend_name.ffi