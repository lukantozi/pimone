from abc import ABC, abstractmethod

class MetricCollector(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    def format_data(self):
        pass

    @abstractmethod
    def collect(self):
        raise NotImplementedError
