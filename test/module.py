from pyvx import vx

def func(*args):
    pass

def PublishKernels(context):
    enum = vx.KERNEL_BASE(vx.ID_DEFAULT, 8) + 1
    kernel = vx.AddKernel(context, b"org.test.module", enum, func, 1, func, func, None, None)
    vx.AddParameterToKernel(kernel, 0, vx.INPUT, vx.TYPE_IMAGE, vx.PARAMETER_STATE_REQUIRED)
    assert vx.FinalizeKernel(kernel) == vx.SUCCESS
    return vx.SUCCESS