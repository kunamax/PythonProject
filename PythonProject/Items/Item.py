from abc import ABC, abstractmethod


class Item(ABC):

    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight


    @abstractmethod
    def use(self, hero):
        pass