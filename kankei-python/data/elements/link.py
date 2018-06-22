from data.elements.abstract_element import AbstractElement


class LinkMeta(type):

    def __repr__(self):
        return f"<class {self.__name__}::Node>"

    def __init__(cls, name, bases, dct):
        super(LinkMeta, cls).__init__(name, bases, dct)
        if name != 'Link':
            setattr(cls, 'type', name)


class Link(AbstractElement):

    def __init__(self, begin_node, end_node, **properties):
        super().__init__(properties)
        self.begin_node = begin_node
        self.end_node = end_node

    @property
    def csv(self):
        csv = self._base_csv
        csv[':TYPE'] = self.type

        csv[':START_ID(%s-ID)' % self.begin_node.label_id_pos] = self.begin_node.id
        csv[':END_ID(%s-ID)' % self.end_node.label_id_pos] = self.end_node.id
        return csv


class SimplifiedLink(Link, metaclass=LinkMeta):
    pass
