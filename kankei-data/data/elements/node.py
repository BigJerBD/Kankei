from data.elements.abstract_element import AbstractElement


class NodeMeta(type):

    def __repr__(self):
        return f"<class {self.__name__}::Node>"

    def __init__(cls, name, bases, dct):
        super(NodeMeta, cls).__init__(name, bases, dct)

        if name != 'Node' and not dct.get('__ignore__', None):
            parent, *rest = bases

            result_labels = dct.get('base_labels', []) + getattr(parent, 'base_labels')
            if dct.get('__ignore_clsname__', None):
                setattr(cls, 'type', dct.get('type', None) or getattr(parent, 'type', []))
            else:
                result_labels = [name] + result_labels
                setattr(cls, 'type', name)

            setattr(cls, 'base_labels', result_labels)
            setattr(cls, 'identifying_label',
                    getattr(cls, "type") if 'identifier' in dct else getattr(parent, 'identifying_label')
                    )

            setattr(cls, 'indexes', getattr(parent, 'indexes', []) + cls.__dict__.get('indexes', []))
            setattr(cls, 'fields', {**getattr(parent, 'fields'), **cls.__dict__.get('fields', {})})


# note ambiguity with type and label
class Node(AbstractElement):
    component_type = 'Node'

    base_labels = []
    valid_extralabels = []
    valid_subcomponents = []
    identifying_label = None

    identifier = None
    indexes = []

    def __init__(self, extra_labels=None, subcomponents=None, all_subcomponents=False, **properties):
        subcomponents = (self.valid_subcomponents if all_subcomponents else subcomponents) or []
        extra_labels = extra_labels or []

        if any(s for s in subcomponents if s not in self.valid_subcomponents):
            raise TypeError("Invalid subnode for node")
        if any(s for s in extra_labels if s not in self.valid_extralabels):
            raise TypeError(f"Invalid extra label for node {''.join(extra_labels)}")

        self.labels = self.base_labels
        self.labels += extra_labels
        for subcomp_cls in subcomponents:
            self.add_subcomponent(subcomp_cls)

        super().__init__(properties)

    def combine(self, other):
        self.props = {**self.props, **other.props}

        missing_labels = [l for l in other.labels if l not in self.labels]
        if missing_labels:
            self.add_subcomponent(other)

    def add_subcomponent(self, subcomp):
        self.labels = list(set(subcomp.base_labels + self.labels))
        self.indexes += list(set(subcomp.indexes + self.indexes))
        self.constraints = list(set(subcomp.constraints + self.constraints))
        self.fields = {**self.fields, **subcomp.fields}

    @property
    def id(self):
        return self.props[self.identifier]

    @property
    def neo4j_csv(self):
        csv = self._base_csv
        id_type = self.fields[self.identifier]
        csv_header = id_type.csv_header(self.identifier)
        csv[':ID(%s-ID)' % self.identifying_label] = csv[csv_header]
        csv[':LABEL'] = ';'.join(self.labels)
        return csv

    @property
    def json(self):
        return self.props


class SimplifiedNode(Node, metaclass=NodeMeta):
    __ignore__ = True
