from pyvx import basic_backend
from pyvx.optimize import OptimizedGraph

class Context(basic_backend.Context):
    def create_graph(self, early_verify):
        return OptimizedGraph(self, early_verify)


