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
        self.combinable_types = combinable_types
        self.uncombined_data = []
        self.combined_data = defaultdict(Node)

    def iter(self, elem):
        yield from self.iter_combined()
        yield from self.yield_uncombined()

    def iter_combined(self):
        yield from self.uncombined_data

    def yield_uncombined(self):
        yield from self.combined_data.values()

    def add(self, elem):
        main_type = elem.labels[-1]
        if main_type in self.combinable_types:
            self.combined_data[elem.id].merge(elem)
        else:
            self.uncombined_data.append(elem)


