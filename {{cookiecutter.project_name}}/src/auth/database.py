import json
import os
from typing import List
from .usermodel import User, UserView

class UserDatabase:
    def __init__(self,path_json: str):
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
                                email=user["email"])
        return None

    

    