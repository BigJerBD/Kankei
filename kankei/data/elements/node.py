from data.elements.abstract_element import AbstractElement


class NodeMeta(type):

    def __repr__(self):
        return f"<class {self.__name__}::Node>"

    def __init__(cls, name, bases, dct):
        super(NodeMeta, cls).__init__(name, bases, dct)

        if name != 'Node' and not dct.get('__ignore__', None):
            parent, *rest = bases

            result_labels = dct.get('labels', []) + getattr(parent, 'labels')
            if dct.get('__ignore_clsname__', None):
                setattr(cls, 'type', dct.get('type', None) or getattr(parent, 'type', []))
            else:
                result_labels = [name] + result_labels
                setattr(cls, 'type', name)

            setattr(cls, 'labels', result_labels)
            setattr(cls, 'concrete_identifier', name if 'identifier' in dct else getattr(
                parent, 'concrete_identifier'))
            setattr(cls, 'indexes', getattr(parent, 'indexes', []) + cls.__dict__.get('indexes', []))
            setattr(cls, 'fields', {**getattr(parent, 'fields'), **cls.__dict__.get('fields', {})})

class Node(AbstractElement):
    concrete_identifier = None
    identifier = None
    labels = []
    indexes = []

    component_type = 'Node'

    def __init__(self, tags=None, **properties):
        self.labels += tags or []
        super().__init__(properties)

    def merge(self, other):

        parent = self.get_generic_parent(other)

        if not self.type:
            self.concrete_identifier = other.concrete_identifier
            self.type = other.type
            self.identifier = other.identifier
        elif parent:
            self.type = parent[-1]

        self.labels = list({l for l in other.labels + self.labels})
        self.indexes += list({l for l in other.indexes + self.indexes})
        self.constraints += list({l for l in other.indexes + self.indexes})
        self.fields = {**self.fields, **other.fields}
        self.props = {**self.props, **other.props}

    def get_generic_parent(self, other):
        return list(set(self.labels).intersection(other.labels))

    @property
    def id(self):
        return self.props[self.identifier]

    @property
    def csv(self):
        csv = self._base_csv
        id_type = self.fields[self.identifier]
        csv_header = id_type.csv_header(self.identifier)
        csv[':ID(%s-ID)' % self.concrete_identifier] = csv[csv_header]
        csv[':LABEL'] = ';'.join(self.labels)
        return csv


class SimplifiedNode(Node, metaclass=NodeMeta):
    __ignore__ = True
