import threading

from pyvx import vx


class VXError(Exception): # FIXME: use different exceptions for different errors
    pass

def _check_status(status):
    if status != 0: # FIXME vx.SUCCSES
        raise VXError(status)

class attribute(object):

    def __init__(self, ctype, enum=None, query=None):
        self.ctype = ctype
        self.enum = enum
        self.query = query

    def __get__(self, instance, owner):
        status, val = self.query(instance.cdata, self.enum, self.ctype)
        _check_status(status)
        return val

    def __set__(self, instance, value):
        print("set",  instance, value) # FXIME

class VxObjectMeta(type):

    def __new__(cls, name, bases, attrs):
        for n, a in  attrs.items():
            if isinstance(a, attribute):
                if a.query is None:
                    a.query = getattr(vx, 'Query' + name)
                if a.enum is None:
                    a.enum = getattr(vx, name.upper() + '_ATTRIBUTE_' + n.upper())
        cls = type.__new__(cls, name, bases, attrs)
        return cls

VxBase = VxObjectMeta('VxBase', (), {})

def _query_ref(reference, attribute, c_type, python_type=None):
    return vx.QueryReference(vx.reference(reference), attribute, c_type, python_type)

class Reference(VxBase):
    count = attribute('vx_uint32', vx.REF_ATTRIBUTE_COUNT, _query_ref)
    type = attribute('vx_enum', vx.REF_ATTRIBUTE_TYPE, _query_ref)

class Context(Reference):
    vendor_id = attribute('vx_uint16')

    _local_state = threading.local()
    _local_state.current_context = None

    def _check_object(self, obj):
        _check_status(vx.GetStatus(vx.reference(obj)))

    def __init__(self):
        self.cdata = vx.CreateContext()
        self.context = self

    def __del__(self):
        vx.ReleaseContext(self.cdata)

    def __enter__(self):
        assert Context._local_state.current_context is None
        Context._local_state.current_context = self
        return self

    def __exit__(self, *args):
        assert Context._local_state.current_context is self
        Context._local_state.current_context = None

