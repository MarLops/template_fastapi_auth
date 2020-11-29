from abc import ABC, abstractmethod
from .usermodel import FullUser

class DBUser(ABC):
    @abstractmethod
    def get_user(self,key):
        ...

    @abstractmethod
    def post(self,user: FullUser):
        ...

    @abstractmethod
    def delete(self, username):
        ...

    @abstractmethod
    def update(self, user: FullUser):
        ...