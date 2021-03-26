from abc import ABC, abstractmethod

class piece(ABC):
    
    @abstractmethod
    def get_valid_positions(self, board_positions, row, column):
        pass
