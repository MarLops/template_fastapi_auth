from abc import ABC, abstractmethod

class DB(ABC):
    @abstractmethod
    def post(self,data):
        ...

    @abstractmethod
    def get_by_key(self,key):
        ...

    @abstractmethod
    def delete_by_key(self,key):
        ...

    @abstractmethod
    def __iter__(self):
        ...