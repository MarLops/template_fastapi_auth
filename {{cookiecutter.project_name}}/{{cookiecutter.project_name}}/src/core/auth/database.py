import json
import os
from typing import List
from .usermodel import FullUser, UserView
from .interface import DBUser

class UserDatabase(DBUser):
    def __init__(self,path_json: str):
        self._path = path_json
        if os.path.exists(path_json):
            with open(path_json, 'r') as myfile:
                self._database = json.loads(myfile.read())
        elif os.path.exists(os.path.join(os.getcwd(),path_json)):
            path_json = os.path.join(os.getcwd(),path_json)
            with open(path_json, 'r') as myfile:
                self._database = json.loads(myfile.read())
            self._path = path_json
        else:
            self._database = {"{{cookiecutter.user}}": {
                                "username": "{{cookiecutter.user}}",
                                "full_name": "{{cookiecutter.full_name}}",
                                "email": "{{cookiecutter.email}}",
                                "password": "{{cookiecutter.password}}",
                                "permition": "admin"
                                }}

    def get_user(self,name: str, password: str):
        if name in self._database:
            user = self._database[name]
            if (user['password'] == password):
                return UserView(username=user["username"],
                                full_name=user["full_name"],
                                email=user["email"],
                                permition=user["permition"])
        return None


    def post(self,user: FullUser):
        user_dict = user.dict()
        if user_dict["username"] in self._database:
            raise ValueError("Already exist this username")
        self._database[user_dict["username"]] = user_dict
        if os.path.exists(self._path):
            with open(self._path, 'w') as myfile:
               myfile.write(json.dumps(self._database))
            return UserView(**user.dict())
    
    def delete(self, username):
        if username in self._database:
            self._database.pop(username)
            if os.path.exists(self._path):
                with open(self._path, 'w') as myfile:
                    myfile.write(json.dumps(self._database))
                    return True
        raise ValueError("Don't exist user")


    def update(self, user: FullUser):
        user_dict = user.dict()
        if user_dict["username"] in self._database:
            self._database[user_dict["username"]] = user_dict
            if os.path.exists(self._path):
                with open(self._path, 'w') as myfile:
                    myfile.write(json.dumps(self._database))
                    return True
        raise ValueError("Don't exist user")
        

        
