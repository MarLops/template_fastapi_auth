from .database import UserDatabase
from .interface import DBUser
from .usermodel import User


class UserPersonal(User):
    ...

class DatabaseUserPersonal(DBUser):
    def get_user(self, key):
        ...

    def post(self, user: User):
        ...


DB_USER = None
    
def create_database_user(config):
    global DB_USER
    path = config.get('DEFAULT','Path_userdatabase')
    DB_USER = UserDatabase(path)


def get_database_user():
    return DB_USER