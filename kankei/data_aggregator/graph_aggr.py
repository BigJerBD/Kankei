from collections.__init__ import defaultdict

from data.elements.node import Node


class graph_aggr:
    """
    Structure that take Kankei Data and organise into a set or not and LINK

    this GraphStructure classifies

    -link by LinkType and how the linktype are connected
    -node by their type, can support also merging type

    struct :

    ['Node:{'Node1': <data>,
           'Node2': <data>,
            ...}
     Link: {'Link1':{Extremities: <data>,
            ...},
    ...]

    """

    def __init__(self):
        self.link = defaultdict(lambda: defaultdict(list))
        self.mergable_node = defaultdict(lambda: defaultdict(Node))
        self.node = defaultdict(list)

    def iter(self):
        yield from self.iter_link()
        yield from self.iter_node()

    def iter_link(self):
        for name, link_dct in self.link.items():
            for sub_name, sub_link_dct in link_dct.items():
                yield f'{name}_{sub_name}', sub_link_dct

    def iter_node(self):
        for name, node_list in self.node.items():
            yield name, node_list

    def add(self, elem):
        if elem.component_type == 'Node':
            self.add_node(elem)
        elif elem.component_type == 'Link':
            self.add_link(elem)

    def add_list(self, data_lst):
        for data in data_lst:
            self.add(data)

    def add_link(self, elem):
        begin_node, end_node = elem.begin_node, elem.end_node
        extremities = f'{begin_node.concrete_identifier}-{end_node.concrete_identifier}'

        self.link[elem.type][extremities].append(elem)

    def add_node(self, elem):
        main_type = elem.labels[-1]
        self.node[main_type].append(elem)
