from pyvx.inc import vx
from pyvx.types import VxError

class attribute(object):
    def __init__(self, enum, vxtype, default=None):
        self.enum = enum
        self.vxtype = vxtype
        self.default = default

    def __get__(self, instance, owner):
        n = '_' + self.name
        if hasattr(instance, n):
            return getattr(instance, n)
        if hasattr(owner, n):
            return getattr(owner, n)
        return self.default

    def __set__(self, instance, value):
        setattr(instance, '_' + self.name, value)
        

class VxObjectMeta(type):
    def __new__(cls, name, bases, attrs):
        attributes = {}
        for b in bases:
            if hasattr(b, '_attributes'):
                attributes.update(b._attributes)
        for n, a in attrs.items():
            if isinstance(a, attribute):
                a.name = n
                attributes[a.enum] = a
        cls = type.__new__(cls, name, bases, attrs)
        cls._attributes = attributes
        return cls

class VxObject(object):
    __metaclass__ = VxObjectMeta


class api(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, fn):
        if not hasattr(fn, 'apis'):
            fn.apis = []
        fn.apis.append(self)
        return fn

class capi(object):
    def __init__(self, cdecl):
        self.cdecl = cdecl

    def __call__(self, fn):
        if not hasattr(fn, 'capis'):
            fn.capis = []
        fn.capis.append(self)
        return fn

##############################################################################

class Reference(VxObject):
    _type = vx.TYPE_REFERENCE

    count = attribute(vx.REF_ATTRIBUTE_COUNT, vx.TYPE_UINT32, 1)
    type =  attribute(vx.REF_ATTRIBUTE_TYPE, vx.TYPE_ENUM, vx.TYPE_REFERENCE)

    def query(self, attribute):
        return vx.SUCCESS, getattr(self, self._attributes[attribute].name)

    def new_handle(self):
        h = vx.ffi.new_handle(self)
        self.context.keep_alive.add(h)
        return h

    def del_handle(self, ptr):
        self.context.keep_alive.remove(ptr)

    def add_log_entry(self, status, message):
        if status != vx.SUCCESS:
            print 'LOG:', status, self, message


@api('QueryReference')
def query(ref, attribute):
    return ref.query(attribute)

@capi('vx_status vxQueryReference(vx_reference, vx_enum, void *, vx_size)')
@capi('vx_status vxQueryContext(vx_context, vx_enum, void *, vx_size)')
def c_query(ref, attribute, ptr, size):
    a = ref._attributes.get(attribute)
    if a is None:
        return vx.FAILURE
    if size != vx.ffi.sizeof(a.vxtype.ctype):
        ref.add_log_entry(vx.FAILURE, "Bad size %d in query, expected %d\n" % (size, vx.ffi.sizeof(a.vxtype.ctype)))
        return vx.FAILURE
    status, value = query(ref, attribute)
    ptr = vx.ffi.cast(a.vxtype.ctype + "*", ptr)
    if isinstance(value, VxObject):
        ptr[0] = ref.context.new_handle(value)
    else:
        ptr[0] = value
    return status

@api('ReleaseReference')
@api('ReleaseContext')
def release(ref):
    pass

@capi('vx_status vxReleaseReference(vx_reference *ref)')
@capi('vx_status vxReleaseContext(vx_context *ref)')
def c_release(ref):
    obj = vx.ffi.from_handle(vx.ffi.cast('void *', ref[0]))
    obj.context.del_handle(ref[0])
    ref[0] = vx.ffi.NULL
    return vx.SUCCESS

@api('AddLogEntry')
def add_log_entry(ref, status, message):
    ref.add_log_entry(status, message)


##############################################################################

class Context(Reference):
    _type = vx.TYPE_CONTEXT

    vendor_id = attribute(vx.CONTEXT_ATTRIBUTE_VENDOR_ID, vx.TYPE_UINT16, vx.ID_DEFAULT)
    version = attribute(vx.CONTEXT_ATTRIBUTE_VERSION, vx.TYPE_UINT16, vx.VERSION)
    unique_kernels = attribute(vx.CONTEXT_ATTRIBUTE_UNIQUE_KERNELS, vx.TYPE_UINT32)
    # FIXME: ...

    def __init__(self):
        self.keep_alive = set()
        self.context = self

    def create_image(self, width, height, color):
        raise NotImplementedError

    def create_graph(self, early_verify):
        raise NotImplementedError

@api('CreateContext')
@capi('vx_context vxCreateContext()')
def create_context():
    from pyvx.optimized_backend import Context
    return Context()

##############################################################################

class Image(Reference):
    _type = vx.TYPE_IMAGE

@api('CreateImage')
@capi('vx_image vxCreateImage(vx_context context, vx_uint32 width, vx_uint32 height, vx_df_image color)')
def create_image(context, width, height, color):
    return context.create_image(width, height, color)

@api('CreateVirtualImage')
@capi('vx_image vxCreateVirtualImage(vx_graph graph, vx_uint32 width, vx_uint32 height, vx_df_image color)')
def create_virtual_image(graph, width, height, color):
    return graph.context.create_virtual_image(graph, width, height, color)

##############################################################################

class Graph(Reference):
    _type = vx.TYPE_GRAPH

    def verify(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

@api('CreateGraph')
@capi('vx_graph vxCreateGraph(vx_context context)')
def create_graph(context, early_verify=True):
    return context.create_graph(early_verify)

@api('VerifyGraph')
@capi('vx_status vxVerifyGraph(vx_graph graph)')
def verify_graph(graph):
    try:
        graph.verify()
    except VxError as e:
        import traceback
        graph.add_log_entry(e.errno, '\n' + traceback.format_exc())
        return e.errno
    return vx.SUCCESS

@api('ProcessGraph')
@capi('vx_status vxProcessGraph(vx_graph graph)')
def process_graph(graph):
    return graph.process()       

##############################################################################

class Node(Reference):
    _type = vx.TYPE_NODE
