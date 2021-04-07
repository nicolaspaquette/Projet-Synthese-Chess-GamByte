from abc import ABC, abstractmethod

class DAO(ABC):
    
    @abstractmethod
    def connection(self):
        pass
