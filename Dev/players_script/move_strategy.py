from abc import ABC, abstractmethod

class move_strategy(ABC):
    
    @abstractmethod
    def select_move(self):
        pass
