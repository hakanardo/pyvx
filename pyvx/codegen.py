"""
:mod:`pyvx.codegen` --- Code generation tools
=============================================

"""

from pycparser import c_parser, c_ast
from pycparser.c_generator import CGenerator
from cffi import FFI
import tempfile, subprocess, os
from shutil import rmtree, copy

typedefs = ''.join("typedef int uint%d_t; typedef int int%d_t;" % (n, n) 
                   for n in [8, 16, 32, 64])

def cparse(code):
    parser = c_parser.CParser()
    ast = parser.parse(typedefs + "void f() {" + code + "}")
    func = ast.ext[-1]
    #func.show()
    assert func.decl.name == 'f'
    return func.body

def cparse_signature(signature):
    parser = c_parser.CParser()
    ast = parser.parse(typedefs + signature + ';')
    ast = ast.ext[-1]
    return ast

class MagicCGenerator(CGenerator):
    def __init__(self, cxnode, magic_vars):
        CGenerator.__init__(self)
        self.cxnode = cxnode
        self.magic_vars = magic_vars

    def visit_StructRef(self, node):
        assert isinstance(node.name, c_ast.ID)
        assert isinstance(node.field, c_ast.ID)
        if node.name.name in self.magic_vars:
            var = self.magic_vars[node.name.name]
            return var.getattr(self.cxnode, node.field.name)
        return CGenerator.visit_StructRef(self, node)

    def visit_ArrayRef(self, node):
        var, channel, index = self.get_magic_array_ref(node)
        if var is None:
            return CGenerator.visit_ArrayRef(self, node)
        return var.getitem(self.cxnode, channel, index)

    def get_magic_array_ref(self, node):
        var_name = None
        if isinstance(node.name, c_ast.StructRef):
            struct = node.name
            assert isinstance(struct.name, c_ast.ID)
            assert isinstance(struct.field, c_ast.ID)
            var_name = struct.name.name
            channel = struct.field.name
        elif isinstance(node.name, c_ast.ID):
            var_name = node.name.name
            channel = None

        if var_name in self.magic_vars:
            var = self.magic_vars[var_name]
            if isinstance(node.subscript, c_ast.ExprList):
                x, y = node.subscript.exprs
                index = (self.visit(x), self.visit(y))
            else:
                index = self.visit(node.subscript)
            return var, channel, index

        return None, None, None

    def visit_Assignment(self, node):
        var, channel, index = self.get_magic_array_ref(node.lvalue)
        if var is None:
            return CGenerator.visit_Assignment(self, node)
        return var.setitem(self.cxnode, channel, index, 
                           node.op, self.visit(node.rvalue))

class Code(object):
    """ 
        Represents some generated C-code together with
        a bit of metadata. It has the following public attributes:

        ``indent_level``
            Number of spaces to indent code added using ``add_block``.
        ``extra_link_args``
            A ``list`` of extra arguments needed to be passed to the linker when 
            compiling the code. It is typically used to link with external libraries 
            used by the code.
        ``includes``
            A ``set`` of lines added at the top of the generated .c file outside
            the function enclosing the code. This is intended for ``#include ...``
            lines.

    """
    
    def __init__(self, code=''):
        """ Construct a new ``Code`` object and initiate it's code to ``code``.            
        """
        self.code = code
        self.indent_level = 0
        self.extra_link_args = []
        self.includes = set()

    def add_block(self, cxnode, code, **magic_vars):
        """ Append ``code`` as a new block of code. It will be enclosed in with ``{}``
            brackets to allow it to declare local variables. The code will be
            parsed and all references to the symbol names passed as keyword 
            arguments will be extracted and handled separately. These magic variables
            are intended to refere to ``Image`` objects, but could be anything that define 
            compatible ``getattr()`` and ``getitem()`` methods. If an ``Image`` is
            passed as the keyword argument ``img``, it can be used in the C-code in 
            the following ways:

                ``img[x,y]``
                    The value of pixel (``x``, ``y``) of a single channel image.
                ``img.channel_x[x,y]``
                    The value of pixel (``x``, ``y``) in ``CHANNEL_X``.
                ``img[i]``
                    The i'th value in the image. ``i`` is an integer between ``0``
                    and ``width * height * channels - 1``.
                ``img.channel_x[i]``
                    The i'th value in ``CAHNNEL_X`` of the image. ``i`` is an integer 
                    between ``0`` and ``width * height - 1``.           
                ``img.width``
                    The width of the image in pixels.
                ``img.height``
                    The height of the image in pixels.                
                ``img.pixels``
                    The number of pixels in the image (``width * height``).
                ``img.values``
                    The number of values in the image (``width * height * channels``).
                ``img.data``
                    A pointer to the beginning of the pixel data.


        """
        ast = cparse(code)
        #ast.show()
        generator = MagicCGenerator(cxnode, magic_vars)
        generator.indent_level = self.indent_level
        hdr = '\n%s// %s\n' % (' ' * self.indent_level, cxnode.__class__.__name__)
        self.code += hdr + generator.visit(ast)

    def add_code(self, code):
        """ Extend the code with ``code`` without any adjustment.
        """        
        self.code += code

    def __str__(self):
        """ Returns the generated code.
        """
        return self.code


def export(signature, add_ret_to_arg=None, retrive_args=True, store_result=True):
    def decorator(f):
        f.signature = signature
        f.add_ret_to_arg = add_ret_to_arg
        f.retrive_args = retrive_args
        f.store_result = store_result
        return staticmethod(f)
    return decorator

class PythonApi(object):
    def __init__(self, api, build=None):
        ffi = self.ffi = FFI()
        ffi.cdef(api.cdef)
        typedefs = []
        code = []
        callbacks = {}
        self.reference_types = set()
        self.enum_types = set()
        for n in dir(api):
            item = getattr(api, n)
            if isinstance(item, Enum):
                typedefs.append(item.typedef(n))
                self.enum_types.add(n)
            elif isinstance(item, Reference):
                s = 'struct _%s *' % n
                typedefs.append('typedef %s %s;' % (s, n))
                self.reference_types.add(s)
        ffi.cdef('\n'.join(typedefs))
        for n in dir(api):
            item = getattr(api, n)
            if hasattr(item, 'signature'):
                fn = item
                tp = ffi._typeof(fn.signature, consider_function_as_funcptr=True)
                callback_var = ffi.getctype(tp, n)
                code.append("%s;" % callback_var)
                callbacks[n] = self.make_callback(tp, fn)
        ffi.cdef('\n'.join(code))
        self.callbacks = callbacks
        api.pyapi = self
        self.api = api
        if build:
            self.build(build, code, typedefs)

    def load(self):
        lib = self.ffi.dlopen(None)
        for n, cb in self.callbacks.items():
            setattr(lib, n, cb)
        self.lib = lib
        self.references = []
        self.freelist = None
        return self


    def make_callback(self, tp, fn):
        store_result = fn.store_result and tp.result.cname in self.reference_types
        if fn.store_result and tp.result.cname in self.enum_types:
            assert not store_result
            enum_result = tp.result.cname
        else:
            enum_result = None
        if fn.retrive_args:       
            retrive_refs = tuple([i for i,a in enumerate(tp.args) 
                                   if a.cname in self.reference_types])
            retrive_enums =  tuple([(i, a.cname) for i,a in enumerate(tp.args) 
                                     if a.cname in self.enum_types])
        else:
            retrive_refs = retrive_enums = ()
        add_ret_to_arg = fn.add_ret_to_arg
        def f(*args):
            args = list(args)
            for i in retrive_refs:
                args[i] = self.retrive(args[i])
            for i, n in retrive_enums:
                args[i] = getattr(self.api, n)[args[i]]
            r = fn(*args)
            if store_result:
                r = self.store(r)
                if add_ret_to_arg is not None:
                    args[add_ret_to_arg].add_reference(r)
            elif enum_result:
                r = getattr(self.api, enum_result).index(r)
            return r
        f.__name__ = fn.__name__
        return self.ffi.callback(tp, f)


    def build(self, (name, version, soversion, out_path), code, typedefs):
        typedefs = '\n'.join(typedefs) + "\n\n"
        tmp = tempfile.mkdtemp()
        try:
            src = os.path.join(tmp, "tmp.c")
            with open(src, 'w') as fd:
                fd.write(""" 
                    #include <stdint.h>
                    #include <Python.h>
                    """ + self.api.cdef + typedefs + """

                    static void __initialize(void) __attribute__((constructor));
                    void __initialize(void) {
                      Py_Initialize();
                      PyEval_InitThreads();                  
                      PyRun_SimpleString("import sys\\n"
                                         "sys.path.append('.')\\n"
                                         "from pyvx.capi import OpenVxApi\\n"
                                         "from pyvx.codegen import PythonApi\\n"
                                         "api = PythonApi(OpenVxApi).load()\\n");
                    }

                    static void __deinitialize(void) __attribute__((destructor));
                    void __deinitialize(void) {
                      Py_Finalize();
                    }
                    """ + '\n'.join(code))

            from distutils.core import Extension
            from cffi.ffiplatform import compile
            fn = compile(tmp, Extension(name='lib' + name, 
                                        sources=[src],
                                        extra_link_args=['-lpython2.7',
                                          '-Wl,-soname,lib%s.so.' % name + soversion]))
            bfn = os.path.join(out_path, os.path.basename(fn))
            full = bfn + '.' + version
            so = bfn + '.' + soversion
            for f in [full, so, bfn]:
                try:
                    os.unlink(f)
                except OSError:
                    pass
            copy(fn, full)
            os.symlink(os.path.basename(full), so)
            os.symlink(os.path.basename(full), bfn)
        finally:
            rmtree(tmp)

        prototypes = '\n'.join('extern ' + l for l in code)
        with open(os.path.join(out_path, name + '.h'), 'w') as fd:
            fd.write("#ifndef __OPENCX_H__\n")
            fd.write("#define __OPENCX_H__\n\n")
            fd.write("#include <stdint.h>\n")
            fd.write(self.api.cdef + '\n')
            fd.write(typedefs + '\n\n')
            fd.write(prototypes + "\n\n")
            fd.write("#endif\n")
        self.library_names = [full, so, bfn]

    def store(self, x):
        "Store the object 'x' and returns a new object descriptor for it."
        p = self.freelist
        if p is None:
            p = len(self.references)
            self.references.append(x)
        else:
            self.freelist = self.references[p]
            self.references[p] = x
        return self.ffi.cast('void *', p)

    def discard(self, p):
        """Discard (i.e. close) the object descriptor 'p'.
        Return the original object that was attached to 'p'."""
        p = int(self.ffi.cast('long', p))
        x = self.references[p]
        self.references[p] = self.freelist
        self.freelist = p
        return x

    def retrive(self, p):
        p = int(self.ffi.cast('long', p))
        return self.references[p]

class Enum(list):
    def __new__(cls, *args, **kwargs):
        return list.__new__(cls, args)
    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.get('prefix', '')
        return list.__init__(self, args)
    def typedef(self, n):
        items = ', '.join('%s=%d' % (self.prefix + e.__name__, i) 
                          for i, e in enumerate(self))
        return 'typedef enum {' + items + '} ' + n + ';'


class Reference(object): pass

                