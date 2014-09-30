from pycparser import c_parser, c_ast
from pycparser.c_generator import CGenerator

def cparse(code):
    parser = c_parser.CParser()
    ast = parser.parse("void f() {" + code + "}")
    func = ast.ext[0]
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
                return var.getitem2d(self.cxnode, channel, self.visit(x), self.visit(y))
            else:
                return var.getitem1d(self.cxnode, channel, self.visit(node.subscript))                

        return CGenerator.visit_ArrayRef(self, node)

class Code(object):
    
    def __init__(self, code=''):
        self.code = code

    def add_block(self, cxnode, code, **magic_vars):
        ast = cparse(code)
        #ast.show()
        generator = MagicCGenerator(cxnode, magic_vars)
        self.code += generator.visit(ast)

    def __str__(self):
        return self.code
