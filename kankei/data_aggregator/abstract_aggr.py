import abc


class AbstractStruct:

    @abc.abstractmethod
    def add(self, elem):
        raise NotImplemented

    @abc.abstractmethod
    def iter(self):
        raise NotImplemented

    @property
    @abc.abstractmethod
    def grouping(self):
        raise NotImplemented
