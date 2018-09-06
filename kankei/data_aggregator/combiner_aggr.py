from collections import defaultdict

from data.elements.node import Node
from data_aggregator.abstract_aggr import AbstractStruct


class CombinerAggr(AbstractStruct):
    """
    struct that receieve data and conbine the necessary one
    by keeping them in memory and

    #note currently only node can be merged
    """

    def __init__(self, combinable_types):
        self.combinable_types = [c.type for c in combinable_types]
        self.uncombined_data = defaultdict(list)
        self.combined_data = defaultdict(lambda: defaultdict(Node))

    def add(self, elem):

        if elem.component_type == "Node":
            main_type = elem.identifying_label
            if main_type in self.combinable_types and elem.id in self.combined_data[main_type]:
                self.combined_data[main_type][elem.id].merge(elem)
            else:
                self.combined_data[main_type][elem.id] = elem
        else:
            self.uncombined_data[elem.type].append(elem)

    def grouping(self):
        return list(self.combined_data.keys())

    def iter(self):
        yield from self.iter_combined()
        yield from self.iter_uncombined()

    def iter_uncombined(self):
        return self.uncombined_data.items()

    def iter_combined(self):
        return ((k, v.values()) for k, v in self.combined_data.items())
