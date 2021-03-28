from abc import ABC, abstractmethod

class player(ABC):
    
    @abstractmethod
    def play_move(self):
        pass
