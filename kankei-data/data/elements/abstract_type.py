import abc


class AbstractType(abc.ABC):

    def __repr__(self):
        return f"Type::{ self.__class__.__name__}"

    def __eq__(self, other):
        return type(self) == type(other)

    @property
    def null(self):
        return ""

    @property
    @abc.abstractmethod
    def csv_type(self):
        ...

    def csv_header(self, name):
        return f'{name}:{self.csv_type}'

    def csv_value(self, value):
        return str(value) if value else ""
