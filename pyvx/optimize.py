from pyvx.backend import *
from pyvx.nodes import *
from collections import defaultdict

class OptimizedGraph(CoreGraph):
    def optimize(self):
        self.consumers = defaultdict(set)
        for node in self.nodes:
            for d in node.inputs + node.inouts:
                self.consumers[d].add(node)

        self.ded_code_removal()

    def ded_code_removal(self):
        worklist = self.images[:]
        while worklist:
            item = worklist.pop()
            if item.optimized_out:
                continue
            if isinstance(item, CoreImage):
                if not item.virtual:
                    continue
                if len(self.consumers[item]) == 0:
                    self.remove_image(item)
                    worklist.append(item.producer)
            elif isinstance(item, Node):
                imgs = item.output_images.values() + item.inout_images.values()
                if all(i.optimized_out for i in imgs):
                    self.remove_node(item)
                    worklist.extend(item.inputs + item.inouts)
            else:
                assert False

    def remove_image(self, img):
        img.optimized_out = True

    def remove_node(self, node):
        node.optimized_out = True
        for d in node.inputs + node.inouts:
            self.consumers[d].remove(node)
