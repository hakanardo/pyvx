from pycparser import c_parser, c_ast
from pycparser.c_generator import CGenerator
from cffi import FFI
import tempfile, subprocess, os

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
    
    def __init__(self, code=''):
        self.code = code
        self.indent_level = 0

    def add_block(self, cxnode, code, **magic_vars):
        ast = cparse(code)
        #ast.show()
        generator = MagicCGenerator(cxnode, magic_vars)
        generator.indent_level = self.indent_level
        hdr = '\n%s// %s\n' % (' ' * self.indent_level, cxnode.__class__.__name__)
        self.code += hdr + generator.visit(ast)

    def add_code(self, code):
        self.code += code

    def __str__(self):
        return self.code


def export(signature):
    def decorator(f):
        f.signature = signature
        return f
    return decorator

class PythonApi(object):
    cdef = ''

    def __init__(self, build=False):
        ffi = self.ffi = FFI()
        ffi.cdef(self.cdef)
        typedefs = []
        code = []
        callbacks = {}
        self.reference_types = set()
        self.enum_types = set()
        for n in dir(self):
            item = getattr(self, n)
            if isinstance(item, Enum):
                items = ', '.join('%s=%d' % (e.__name__, i) 
                                  for i, e in enumerate(item))
                typedefs.append('typedef enum {' + items + '} ' + n + ';')
                self.enum_types.add(n)
            elif isinstance(item, Reference):
                s = 'struct _%s *' % n
                typedefs.append('typedef %s %s;' % (s, n))
                self.reference_types.add(s)
        ffi.cdef('\n'.join(typedefs))
        for n in dir(self):
            item = getattr(self, n)
            if hasattr(item, 'signature'):
                fn = item
                tp = ffi._typeof(fn.signature, consider_function_as_funcptr=True)
                callback_var = ffi.getctype(tp, n)
                code.append("%s;" % callback_var)
                callbacks[n] = self.make_callback(tp, fn)
        self._code = code
        self._typedefs = typedefs
        ffi.cdef('\n'.join(code))
        if not build:
            lib = ffi.dlopen(None)
            for n, cb in callbacks.items():
                setattr(lib, n, cb)
            self._lib = lib
            self._ffi = ffi
            self._callbacks = callbacks

        self.references = []
        self.freelist = None
        self.ffi = ffi

    def make_callback(self, tp, fn):
        store_result = tp.result.cname in self.reference_types
        retrieve_refs = tuple([i for i,a in enumerate(tp.args) 
                               if a.cname in self.reference_types])
        retrieve_enums =  tuple([(i, a.cname) for i,a in enumerate(tp.args) 
                                 if a.cname in self.enum_types])
        def f(*args):
            args = list(args)
            for i in retrieve_refs:
                args[i] = self.retrive(args[i])
            for i, n in retrieve_enums:
                args[i] = getattr(self, n)[args[i]]
            r = fn(*args)
            if store_result:
                r = self.store(r)
            return r
        return self.ffi.callback(tp, f)


    def build(self, name):
        tmp = tempfile.mkdtemp()
        pwd = os.getcwd()
        os.chdir(tmp)
        typedefs = '\n'.join(self._typedefs) + "\n\n"

        with open("tmp.c", 'w') as fd:
            fd.write(""" 
                #include <stdint.h>
                #include <Python.h>
                """ + typedefs + """

                static void __initialize(void) __attribute__((constructor));
                void __initialize(void) {
                  Py_Initialize();
                  PyRun_SimpleString("import sys\\n"
                                     "sys.path.append('.')\\n"
                                     "from pyvx.capi import OpenVxApi\\n"
                                     "api = OpenVxApi()\\n");
                }

                static void __deinitialize(void) __attribute__((destructor));
                void __deinitialize(void) {
                  Py_Finalize();
                }
                """ + '\n'.join(self._code))
        subprocess.call(['gcc', '-c', '-fPIC', '-I/usr/include/python2.7', 'tmp.c'])
        subprocess.call(['gcc', '-shared', '-Wl,-soname,lib%s.so' % name,
                         '-o', '%s/lib%s.so' % (pwd, name), 'tmp.o', '-lpython2.7'])
        os.chdir(pwd)
        subprocess.call(['rm', '-r', tmp])

        prototypes = '\n'.join('extern ' + l for l in self._code)
        with open(name + '.h', 'w') as fd:
            fd.write("#ifndef __OPENCX_H__\n")
            fd.write("#define __OPENCX_H__\n\n")
            fd.write("#include <stdint.h>\n")
            fd.write(self.cdef + '\n')
            fd.write(typedefs + '\n\n')
            fd.write(prototypes + "\n\n")
            fd.write("#endif\n")

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
    def __new__(cls, *args):
        return list.__new__(cls, args)
    def __init__(self, *args):
        return list.__init__(self, args)

class Reference(object): pass

                