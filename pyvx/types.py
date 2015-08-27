from pyvx._auto import _VXAuto
from pyvx import __backend_version__

class VXTypes(_VXAuto):
    def __init__(self, backend):
        if backend.ffi.string(backend.lib._get_backend_version()) != __backend_version__:
            raise ImportError("Backend version missmatch. Please recompile it using:\n\n" +
                              "    python -mpyvx.build_cbackend %s %s\n" % (backend.ffi.string(backend.lib._get_backend_name()),
                                                                            backend.ffi.string(backend.lib._get_backend_install_path())))

        _VXAuto.__init__(self, backend.ffi, backend.lib)
        self.SCALE_PYRAMID_HALF = 0.5
        self.SCALE_PYRAMID_ORB = 0.8408964
        self.FMT_REF = self._ffi.string(self._lib._get_FMT_REF())
        self.FMT_SIZE = self._ffi.string(self._lib._get_FMT_SIZE())

    def KERNEL_BASE(self, vendor, lib):
        return self._lib._get_KERNEL_BASE(vendor, lib)

    def imagepatch_addressing_t(self, dim_x=0, dim_y=0, stride_x=0, stride_y=0, scale_x=0, scale_y=0, step_x=0, step_y=0):
        return self._ffi.new("vx_imagepatch_addressing_t *", (dim_x, dim_y, stride_x, stride_y, scale_x, scale_y, step_x, step_y))


    def perf_t(self, tmp=0, beg=0, end=0, sum=0, avg=0, min=0, num=0, max=0):
        return self._ffi.new("vx_perf_t *", (tmp, beg, end, sum, avg, min, num, max))


    def kernel_info_t(self, enumeration, name):
        s = self._ffi.new("vx_kernel_info_t *")
        s.enumeration = enumeration
        assert len(name) < self.MAX_KERNEL_NAME
        s.name[0:len(name)] = name
        s.name[len(name)] = '\0'
        return s


    def border_mode_t(self, mode, constant_value=0):
        return self._ffi.new("vx_border_mode_t *", (mode, constant_value))


    def keypoint_t(self, x, y, strength, scale, orientation, tracking_status, error):
        return self._ffi.new("vx_keypoint_t *", (x, y, strength, scale, orientation, tracking_status, error))


    def rectangle_t(self, start_x, start_y, end_x, end_y):
        return self._ffi.new("vx_rectangle_t *", (start_x, start_y, end_x, end_y))


    def delta_rectangle_t(self, delta_start_x, delta_start_y, delta_end_x, delta_end_y):
        return self._ffi.new("vx_delta_rectangle_t *", (delta_start_x, delta_start_y, delta_end_x, delta_end_y))


    def coordinates2d_t(self, x, y):
        return self._ffi.new("vx_coordinates2d_t *", (x, y))


    def coordinates3d_t(self, x, y, z):
        return self._ffi.new("vx_coordinates3d_t *", (x, y, z))

