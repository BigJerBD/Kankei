from data.elements.abstract_element import AbstractElement


class NodeMeta(type):

    def __repr__(self):
        return f"<class {self.__name__}::Node>"

    def __init__(cls, name, bases, dct):
        super(NodeMeta, cls).__init__(name, bases, dct)
        if name != 'SimplifiedNode':
            parent, *rest = bases
            setattr(cls, 'labels', [name] + getattr(cls, 'labels'))
            setattr(cls, 'type', name)
            setattr(cls, 'label_id_pos', name if 'identifier' in dct else getattr(parent, 'label_id_pos'))
            setattr(cls, 'indexes', getattr(parent, 'indexes', []) + cls.__dict__.get('indexes', []))
            setattr(cls, 'fields', {**getattr(parent, 'fields'), **cls.__dict__.get('fields')})


class Node(AbstractElement):
    label_id_pos = None
    identifier = None
    labels = []
    indexes = []

    def __init__(self, **properties):
        super().__init__(properties)

    def __iadd__(self, other):
        # todo add verification?
        self.identifier = other.identifier
        self.label_id_pos = other.label_id_pos
        self.labels = list({l for l in other.labels + self.labels})
        self.indexes += list({l for l in other.indexes + self.indexes})
        self.constraints += list({l for l in other.indexes + self.indexes})
        self.fields = {**self.fields, **other.fields}
        self.props = {**self.props, **other.props}

        return self

    @property
    def id(self):
        return self.props[self.identifier]

    @property
    def csv(self):
        csv = self._base_csv
        id_type = self.fields[self.identifier]
        csv_header = id_type.csv_header(self.identifier)
        csv[':ID(%s-ID)' % self.label_id_pos] = csv.pop(csv_header)
        csv[':LABEL'] = ';'.join(self.labels)
        return csv


class SimplifiedNode(Node, metaclass=NodeMeta): ...
