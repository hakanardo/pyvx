from pyvx.api import VX, VXU
try:
    from pyvx._default import backend
except ImportError:
    raise ImportError("No default backend found. Please build one using:\n\n" +
                      "    python -mpyvx.build_cbackend --default name /path/to/openvx/install\n" +
                      "")
vx = VX(backend)
vxu = VXU(backend)
