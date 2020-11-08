import json
import os
from typing import List
from .usermodel import User, UserView
from .interface import DBUser

class UserDatabase(DBUser):
    def __init__(self,path_json: str):
        self._path = path_json
        if os.path.exists(path_json):
            with open(path_json, 'r') as myfile:
                self._database = json.loads(myfile.read())
        else:
            raise Exception("There is not a database")

    def get_user(self,name: str, password: str):
        if name in self._database:
            user = self._database[name]
            if (user['password'] == password):
                return UserView(name=user["username"],
                                full_name=user["full_name"],
                                email=user["email"],
                                permition=user["permition"]])
        return None
    
    def post(self,user: User):
        self._database.update(user["name"],user.dict())

    def __del__(self):
        if os.path.exists(self._path):
            with open(self._path, 'w') as myfile:
               myfile.write(json.dump(self._database))
        del self


class PersonalDatabase(DBUser):
    def get_user(self, key):
        ...

    def post(self, user: User):
        ...

    
def get_database(path):
    return UserDatabase(path)