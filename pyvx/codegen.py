from pycparser import c_parser, c_ast
from pycparser.c_generator import CGenerator

import cffi
from cffi import FFI
from cffi.verifier import Verifier
import types, tempfile, subprocess, os

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
        return staticmethod(f)
    return decorator

class PythonApi(object):
    def __init__(self, build=False):
        ffi = FFI()
        code = []
        callbacks = {}
        for n in dir(self):
            fn = getattr(self, n)
            #if isinstance(fn, types.FunctionType) and hasattr(fn, 'signature'):
            if hasattr(fn, 'signature'):
                tp = ffi._typeof(fn.signature, consider_function_as_funcptr=True)
                callback_var = ffi.getctype(tp, n)
                code.append("%s;" % callback_var)
                callbacks[n] = ffi.callback(tp, fn)
        self._code = code
        ffi.cdef('\n'.join(code))
        if not build:
            lib = ffi.dlopen(None)
            for n, cb in callbacks.items():
                setattr(lib, n, cb)
            self._lib = lib
            self._ffi = ffi
            self._callbacks = callbacks

    def build(self, name):
        tmp = tempfile.mkdtemp()
        pwd = os.getcwd()
        os.chdir(tmp)

        with open("tmp.c", 'w') as fd:
            fd.write("""
                #include <Python.h>

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
            fd.write(prototypes + "\n\n")
            fd.write("#endif\n")
