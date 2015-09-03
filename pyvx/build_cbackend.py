import os, re, sys
from cffi import FFI
from pyvx import __backend_version__

mydir = os.path.dirname(os.path.abspath(__file__))

def build(name, openvx_install, default):
    pwd = os.getcwd()
    os.chdir(os.path.dirname(mydir))
    assert name != 'default'

    hdr = os.path.join(openvx_install, 'include', 'VX', 'vx.h')
    if not os.path.exists(hdr):
        print "ERROR: Can't find header", hdr
        exit(-1)

    lib = os.path.join(openvx_install, 'bin', 'libopenvx.so')
    if not os.path.exists(lib):
        print "ERROR: Can't find lib", lib
        exit(-1)

    defs= dict(VX_API_ENTRY='', VX_API_CALL='', VX_CALLBACK='', VX_MAX_KERNEL_NAME='256')
    if os.name == 'nt':
        defs['VX_API_CALL'] = '__stdcall'
        defs['VX_CALLBACK'] = '__stdcall'

    ffi = FFI()

    # vx.h
    vx = open(os.path.join(mydir, "cdefs", "vx.h")).read()
    vx = re.subn(r'(#define\s+[^\s]+)\s.*', r'\1 ...', vx)[0] # Remove specifics from #defines
    ffi.cdef(vx)

    # vx_vendors.h
    ffi.cdef(open(os.path.join(mydir, "cdefs", "vx_vendors.h")).read())

    # vx_types.h
    types = open(os.path.join(mydir, "cdefs", "vx_types.h")).read()

    for k,v in defs.items():
        types = types.replace(k, v)

    types = re.subn(r'(#define\s+[^\s]+)\s.*', r'\1 ...', types)[0] # Remove specifics from #defines
    types = re.subn(r'(\/\*.*?\*\/)', r'', types)[0] # Remove some one line comments
    types = re.subn(r'=.*,', r'= ...,', types)[0] # Remove specifics from enums
    types = re.subn(r'\[\s*[^\s]+?.*?\]', r'[...]', types)[0] # Remove specific array sizes

    ffi.cdef(types)
    ffi.cdef('''
        char *_get_FMT_REF(void);
        char *_get_FMT_SIZE(void);
        int _get_KERNEL_BASE(int vendor, int lib);
        char *_get_backend_version();
        char *_get_backend_name();
        char *_get_backend_install_path();
    ''')

    # vx_kernels.h
    kernels = open(os.path.join(mydir, "cdefs", "vx_kernels.h")).read()
    kernels = re.subn(r'=.*,', r'= ...,', kernels)[0] # Remove specifics from enums
    ffi.cdef(kernels)

    # vx_api.h
    api = open(os.path.join(mydir, "cdefs", "vx_api.h")).read()
    for k, v in defs.items():
        api = api.replace(k, v)
    ffi.cdef(api)

    # vx_nodes.h
    nodes = open(os.path.join(mydir, "cdefs", "vx_nodes.h")).read()
    for k, v in defs.items():
        nodes = nodes.replace(k, v)
    ffi.cdef(nodes)

    # vxu.h
    vxu = open(os.path.join(mydir, "cdefs", "vxu.h")).read()
    for k, v in defs.items():
        vxu = vxu.replace(k, v)
    ffi.cdef(vxu)

    ffi.set_source("pyvx.backend.%s" % name, """
        #include <VX/vx.h>
        #include <VX/vxu.h>
        char *_get_FMT_REF(void) {return VX_FMT_REF;}
        char *_get_FMT_SIZE(void) {return VX_FMT_SIZE;}
        int _get_KERNEL_BASE(int vendor, int lib) {return VX_KERNEL_BASE(vendor, lib);}
        char *_get_backend_version() {return "%s";}
        char *_get_backend_name() {return "%s";}
        char *_get_backend_install_path() {return "%s";}
                   """ % (__backend_version__, name, openvx_install),
                   include_dirs=[os.path.join(openvx_install, 'include')],
                   library_dirs=[os.path.join(openvx_install, 'bin')],
                   extra_link_args=['-Wl,-rpath=' + os.path.abspath(os.path.join(openvx_install, 'bin'))],
                   libraries=['openvx', 'vxu'])
    ffi.compile()

    default_file_name = os.path.join('pyvx', 'backend', '_default.py')
    if default or not os.path.exists(default_file_name):
        fd = open(default_file_name, 'w')
        fd.write("from pyvx.backend.%s import ffi, lib\n" % name)
        fd.close()

        import pyvx.backend as backend
        assert backend.ffi.string(backend.lib._get_backend_version()) == __backend_version__
        assert backend.ffi.string(backend.lib._get_backend_name()) == name
        assert backend.ffi.string(backend.lib._get_backend_install_path()) == openvx_install

    exec "import pyvx.backend.%s as backend" % name
    assert backend.ffi.string(backend.lib._get_backend_version()) == __backend_version__
    assert backend.ffi.string(backend.lib._get_backend_name()) == name
    assert backend.ffi.string(backend.lib._get_backend_install_path()) == openvx_install

    print
    print "Succesfully built backend pyvx.backend.%s in %s" % (name, mydir)
    print


if __name__ == '__main__':
    args = sys.argv[1:]
    default = '--default' in args
    if default:
        args.remove('--default')
    if len(args) == 2:
        name, openvx_install = args
        build(name, openvx_install, default)
    else:
        print "Usage: %s [--default] <name> <openvx install path>" % sys.argv[0]
