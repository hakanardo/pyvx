from pyvx.backend import *
from pyvx.nodes import *
from collections import defaultdict
from itertools import combinations

class OptimizedGraph(CoreGraph):
    def optimize(self):
        self.identify_consumers()
        self.identify_relations()
        self.merge_elementwise_nodes()
        self.ded_code_removal()

    def identify_consumers(self):
        self.consumers = defaultdict(set)
        for node in self.nodes:
            for d in node.inputs + node.inouts:
                self.consumers[d].add(node)

    def identify_relations(self):
        for node in self.nodes:
            node.parents = set()
            node.children = set()
        for node in self.nodes:
            for d in node.inputs:
                if hasattr(d, 'producer') and d.producer is not None:
                    node.parents.add(d.producer)
                    d.producer.children.add(node)

    def remove_image(self, img):
        img.optimized_out = True

    def remove_node(self, node):
        node.optimized_out = True
        for d in node.inputs + node.inouts:
            self.consumers[d].remove(node)
        self.nodes.remove(node)

    def ded_code_removal(self):
        worklist = list(self.images)
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
                    worklist.extend(item.input_images.values())
                    worklist.extend(item.inout_images.values())
            else:
                assert False

    def merge_elementwise_nodes(self):
        scheduler = Scheduler(self.nodes, self.images)
        active_group = []
        delayed_nodes = []
        while scheduler.blocked_nodes:
            while scheduler.loaded_nodes:
                node = scheduler.loaded_nodes.pop()
                if isinstance(node, ElementwiseNode):
                    active_group.append(node)
                    scheduler.fire(node)
                else:
                    for n in node.parents:
                        if n in active_group:
                            delayed_nodes.append(node)
                            break
                    else:
                        scheduler.fire(node)
            if len(active_group) == 1:
                scheduler.fire(active_group[0])
            elif len(active_group) > 1:
                for n in active_group:
                    self.nodes.remove(n)
                scheduler.fire(MergedElementwiseNode(self, active_group))
            active_group = []
            for n in delayed_nodes:
                scheduler.fire(n)
            delayed_nodes = []

        # Restore invariants
        self.nodes = self.schedule()
        self.identify_consumers()
        self.identify_relations()

