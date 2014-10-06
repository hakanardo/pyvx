from codegen import PythonApi, export, Enum, Reference
from pyvx import *


class OpenVxApi(object):
    
    vx_context = Reference()
    vx_image = Reference()

    vx_fourcc = Enum(FOURCC_VIRT, FOURCC_RGB, FOURCC_RGBX, FOURCC_UYVY,
                     FOURCC_YUYV, FOURCC_U8, FOURCC_S8, FOURCC_U16, 
                     FOURCC_S16, FOURCC_U32, FOURCC_S32)

    @export("vx_context()")
    def vxCreateContext():
        return Context()

    @export("vx_image(vx_context, uint32_t, uint32_t, vx_fourcc)")
    def vxCreateImage(context, width, height, color):
        print color
        img = Image(width, height, color, context=context)
        # FIXME: context.free_on_del.add(img)
        return img

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'build' and len(sys.argv) == 3:
        api = PythonApi(OpenVxApi, build=sys.argv[2])
    else:
        print 'Usage: %s build <lib>' % sys.argv[0]
