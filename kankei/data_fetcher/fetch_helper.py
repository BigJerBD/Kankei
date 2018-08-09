from collections import defaultdict
from xml.etree import ElementTree as Et

from data import node_groups
from data.elements.node import Node


def xml_parse(method):
    """
    decorator for xml that give data in graph
    :param method:
    :return:
    """

    def wrap(xml_path, fetch_helper):
        data_root = Et.parse(xml_path).getroot()
        data = defaultdict(list)
        method(data_root, fetch_helper)
        return data

    return wrap


class KankeiSmartDict:
    """
    dictionary that place automatically the object depending on the class.
    struct :

    ['Node:{'Node1': <data>,
           'Node2': <data>,
            ...}
     Link: {'Link1':{SubTypeLink: <data>,
            ...},
    ...]
    """
    node_groups = node_groups()

    def __init__(self):
        self._data = {
            'Node': defaultdict(lambda: defaultdict(Node)),
            'Link': defaultdict(lambda: defaultdict(list))
        }

    def iter_link(self):
        for name, link_dct in self.data['Link'].items():
            for sub_name, sub_link_dct in link_dct.items():
                yield f'{name}_{sub_name}', sub_link_dct

    def iter_node(self):
        for name, node_dict in self.data['Node'].items():
            yield name, node_dict.values()

    @property
    def data(self):
        return self._data

    def add_list(self, data_lst):
        for data in data_lst:
            self.add(data)

    def add(self, elem):
        if elem.component_type == 'Node':
            self.add_node(elem)
        elif elem.component_type == 'Link':
            self.add_link(elem)

    def add_link(self, elem):
        begin_node, end_node = elem.begin_node, elem.end_node
        extremities = f'{begin_node.concrete_identifier}-{end_node.concrete_identifier}'

        self._data['Link'][elem.type][extremities].append(elem)

    def add_node(self, elem):
        main_type = elem.labels[-1]

        if main_type in (grp.type for grp in self.node_groups.keys()):
            self._data['Node'][main_type][elem.id].merge(elem)
        else:
            self._data['Node'][main_type][elem.id] = elem
