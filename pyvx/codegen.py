from pycparser import c_parser, c_ast
from pycparser.c_generator import CGenerator

def cparse(code):
    parser = c_parser.CParser()
    typedefs = ''.join("typedef int uint%d_t; typedef int int%d_t;" % (n, n) 
                       for n in [8, 16, 32, 64])
    ast = parser.parse(typedefs + "void f() {" + code + "}")
    func = ast.ext[-1]
    #func.show()
    assert func.decl.name == 'f'
    return func.body

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

    def add_block(self, cxnode, code, **magic_vars):
        ast = cparse(code)
        #ast.show()
        generator = MagicCGenerator(cxnode, magic_vars)
        hdr = '\n// %s\n' % cxnode.__class__.__name__
        self.code += hdr + generator.visit(ast)

    def __str__(self):
        return self.code
