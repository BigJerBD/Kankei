"""
All data related to Kankei
"""
import inspect as inspect
import sys
from collections import defaultdict

from data import links, nodes
from data.elements import proprety_types
from data.elements.abstract_type import AbstractType
from data.elements.link import Link
from data.elements.node import SimplifiedNode


def _get_classes(cls, from_module):
    return [cur_cls for _, cur_cls in inspect.getmembers(sys.modules[from_module], inspect.isclass)
            if cls in cur_cls.__mro__[1:]
            ]


def _get_node_group(classes):
    groups = defaultdict(list)
    for cls in classes:
        direct_parent, *rest = cls.__bases__
        if direct_parent != SimplifiedNode:
            groups[direct_parent].append(cls)
    return groups


def all_links():
    return _get_classes(Link, 'data.links')


def all_nodes():
    return _get_classes(SimplifiedNode, 'data.nodes')


def all_types():
    return _get_classes(AbstractType, 'data.elements.proprety_types')


def node_groups():
    return _get_node_group(all_nodes())
