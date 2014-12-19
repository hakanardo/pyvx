from pyvx.inc.vx import *
from pyvx import model
from pyvx.nodes import *

for n in dir(model):
    func = getattr(model, n)
    if hasattr(func, 'apis'):
        for api in func.apis:
            name = api.name
            locals()[name] = func

