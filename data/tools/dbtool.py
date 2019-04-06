from abc import ABC, abstractmethod
from constants import *

class DBTool(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_db(self):
        pass

    @abstractmethod
    def register(self, id, command=NO_ACTION, save=True):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def upload_to_db(self, file_name, save=True):
        pass

    @abstractmethod
    def get_all(self):
        pass
