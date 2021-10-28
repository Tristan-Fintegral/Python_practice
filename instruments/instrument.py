from abc import ABC, abstractmethod

class BaseInstrument(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def price(self, market_data_object):
        raise NotImplementedError()