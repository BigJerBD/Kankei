import abc


class AbstractStruct:

    @abc.abstractmethod
    def add(self, elem):
        raise NotImplemented

    @abc.abstractmethod
    def iter(self, elem):
        raise NotImplemented
