from abc import ABC, abstractmethod

class PriorityQueue(ABC):
    @abstractmethod
    def insert(self, key, value):
        pass

    @abstractmethod
    def find_min(self):
        pass

    @abstractmethod
    def extract_min(self):
        pass

    @abstractmethod
    def decrease_key(self, node, new_key):
        pass

    @abstractmethod
    def meld(self, other):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    def delete(self, node):
        # Шаблонный метод через decrease_key и extract_min
        self.decrease_key(node, float('-inf'))
        self.extract_min()