from .database import UserDatabase
from .interface import DBUser
from .usermodel import FullUser, UserView


class UserPersonal(UserView):
    ...

class DatabaseUserPersonal(DBUser):
    def get_user(self, key) -> UserPersonal:
        return UserPersonal()

    def post(self, user: FullUser) -> None:
        ...


DB_USER = None
    
def create_database_user(*arg,**kwargs):
    global DB_USER
    DB_USER = UserDatabase(*arg)


def get_database_user() -> DBUser:
    return DB_USER