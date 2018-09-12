"""
All data related to Kankei
"""
import inspect as inspect
import sys

from data import links, nodes
from data.elements import proprety_types
from data.elements.abstract_type import AbstractType
from data.elements.link import Link
from data.elements.node import SimplifiedNode


def _get_classes(cls, from_module):
    return {cur_cls.__name__: cur_cls
            for _, cur_cls in inspect.getmembers(sys.modules[from_module], inspect.isclass)
            if cls in cur_cls.__mro__[1:]
            }


all_links = _get_classes(Link, 'data.links')

all_nodes = _get_classes(SimplifiedNode, 'data.nodes')

all_types = _get_classes(AbstractType, 'data.elements.proprety_types')
