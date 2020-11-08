from abc import ABC, abstractmethod
from .usermodel import User

class DBUser(ABC):
    @abstractmethod
    def get_user(self,key):
        ...

    @abstractmethod
    def post(self,user: User):
        ...