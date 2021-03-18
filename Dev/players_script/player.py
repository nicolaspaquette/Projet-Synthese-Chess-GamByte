from abc import ABC, abstractmethod

class player(ABC):
    
    @abstractmethod
    def choose_move(self):
        pass
