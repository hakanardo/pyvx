from pyvx.backend import *
from pyvx.nodes import *
from collections import defaultdict
from itertools import combinations

class OptimizedGraph(CoreGraph):
    def optimize(self):
        self.identify_consumers()
        self.ded_code_removal()
        self.identify_relations()
        self.merge_elementwise_nodes()

    def identify_consumers(self):
        self.consumers = defaultdict(set)
        for node in self.nodes:
            for d in node.inputs + node.inouts:
                self.consumers[d].add(node)

    def identify_relations(self):
        for node in self.nodes:
            node.parents = set()
            node.children = set()
            node.ancestors = set()
        for node in self.nodes:
            for d in node.inputs:
                if hasattr(d, 'producer') and d.producer is not None:
                    node.parents.add(d.producer)
                    node.ancestors |= d.producer.ancestors
                    d.producer.children.add(node)
        for node in self.nodes:
            Group(node)

    def remove_image(self, img):
        img.optimized_out = True
        self.images.remove(img)

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
                    worklist.extend(item.inputs + item.inouts)
            else:
                assert False

    def merge_elementwise_nodes(self):
        nodes = [n for n in self.nodes if isinstance(n, ElementwiseNode)]
        retry = True
        while retry:
            retry = False
            for n1, n2 in combinations(nodes, 2):
                if n1.group is n2.group:
                    continue
                if self.mergable(n1, n2):
                    n1.group.merge(n2.group)
                    retry = True

        groups = set()
        for n in self.nodes:
            if len(n.group.nodes) > 1:
                groups.add(n.group)
        for grp in groups:
            for n in grp.nodes:
                self.nodes.remove(n)
            MergedElementwiseNode(self, grp.nodes)

        # Restore invariants
        self.nodes = self.schedule()
        self.identify_consumers()
        self.identify_relations()

    def mergable(self, node1, node2):
        common_parents = node1.group.parents & node2.group.parents
        common_children = node1.group.children & node2.group.children
        if len(common_parents) == 0 and len(common_children) == 0:
            # Its possible but probably not beneficial to merge in this case
            return False 

        common_ancestors = node1.group.ancestors & node2.group.ancestors
        for ancestor in node1.group.ancestors - common_ancestors:
            for n in ancestor.ancestors:
                if n.group is node2.group:
                    return False
        for ancestor in node2.group.ancestors - common_ancestors:
            for n in ancestor.ancestors:
                if n.group is node1.group:
                    return False
        return True


class Group(object):
    def __init__(self, *nodes):
        self.nodes = []
        self.parents, self.children, self.ancestors = set(), set(), set()
        self.add(nodes)

    def add(self, nodes):
        for n in nodes:
            self.nodes.append(n)
            self.parents |= n.parents
            self.children |= n.children
            self.ancestors |= n.ancestors
            n.group = self

    def merge(self, group):
        self.add(group.nodes)