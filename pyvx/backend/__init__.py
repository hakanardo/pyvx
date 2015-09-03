try:
    from pyvx.backend._default import lib, ffi
except ImportError:
    raise ImportError("No default backend found. Please build one using:\n\n" +
                      "    python -mpyvx.build_cbackend --default name /path/to/openvx/install\n" +
                      "")
