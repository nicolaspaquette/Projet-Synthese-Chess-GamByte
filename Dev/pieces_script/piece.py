from abc import ABC, abstractmethod

class piece(ABC):

    @abstractmethod
    def get_valid_moves(self):
        pass
