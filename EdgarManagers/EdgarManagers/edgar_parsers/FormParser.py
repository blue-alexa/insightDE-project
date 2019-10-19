from abc import ABCMeta, abstractmethod

class AbstractFormParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, source, source_name):
        pass