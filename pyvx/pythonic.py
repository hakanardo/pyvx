import threading

class VXError(Exception): # FIXME: use different exceptions for different errors
    pass

def _check_status(status):
    if status != 0: # FIXME vx.SUCCSES
        raise VXError(status)

class attribute(object):

    def __init__(self, ctype, enum_name=None, cast_to_ref=False):
        self.ctype = ctype
        self.enum_name = enum_name
        self.cast_to_ref = cast_to_ref

    def __get__(self, instance, owner):
        vx = instance.context.vx
        cdata = instance.cdata
        if self.cast_to_ref:
            cdata = vx.reference(cdata)
        query = getattr(vx, self.query)
        enum = getattr(vx, self.enum_name)
        status, val = query(cdata, enum, self.ctype)
        _check_status(status)
        return val

    def __set__(self, instance, value):
        print "set",  instance, value

class VxObjectMeta(type):

    def __new__(cls, name, bases, attrs):
        for n, a in  attrs.items():
            if isinstance(a, attribute):
                a.query = 'Query' + name
                if a.enum_name is None:
                    a.enum_name = name.upper() + '_ATTRIBUTE_' + n.upper()
        cls = type.__new__(cls, name, bases, attrs)
        return cls


class Reference(object):
    __metaclass__ = VxObjectMeta
    count = attribute('vx_uint32', 'REF_ATTRIBUTE_COUNT', True) # FIXME: use enum instead of strings
    type = attribute('vx_enum', 'REF_ATTRIBUTE_TYPE', True)

class Context(Reference):
    vendor_id = attribute('vx_uint16')

    _local_state = threading.local()
    _local_state.current_context = None

    def _check_object(self, obj):
        _check_status(self.vx.GetStatus(self.vx.reference(obj)))

    def __init__(self, vx=None):
        if vx is None:
            from pyvx.default import vx
        self.vx = vx
        self.cdata = vx.CreateContext()
        self.context = self

    def __del__(self):
        self.vx.ReleaseContext(self.cdata)

    def __enter__(self):
        assert Context._local_state.current_context is None
        Context._local_state.current_context = self
        return self

    def __exit__(self, *args):
        assert Context._local_state.current_context is self
        Context._local_state.current_context = None

