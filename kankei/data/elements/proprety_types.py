from data.elements.abstract_type import AbstractType


class Int(AbstractType):

    @property
    def csv_type(self):
        return 'int'


class Long(AbstractType):

    @property
    def csv_type(self):
        return 'long'


class Float(AbstractType):

    @property
    def csv_type(self):
        return 'float'


class Double(AbstractType):

    @property
    def csv_type(self):
        return 'double'


class String(AbstractType):

    @property
    def csv_type(self):
        return 'string'


class Boolean(AbstractType):

    @property
    def csv_type(self):
        return 'boolean'

    def csv_value(self, value):
        return str(value).lower() if value else ""


class List(AbstractType):

    def __init__(self, contained_type=None):
        super().__init__()
        self._contained_type = contained_type

    @property
    def contained_type(self):
        return self._contained_type

    @property
    def csv_type(self):
        return '%s[]' % self.contained_type.csv_type

    @property
    def null(self):
        return []

    def csv_value(self, value):
        return ';'.join(str(x) for x in value)

    def __eq__(self, other):
        if type(self) == type(other):
            return (self.contained_type is None or
                    other.contained_type is None or
                    self.contained_type == other.contained_type
                    )
        return False
