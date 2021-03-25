from abc import ABC, abstractmethod

class piece(ABC):
    
    @abstractmethod
    def is_move_valid(self):
        pass
