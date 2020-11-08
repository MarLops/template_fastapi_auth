import os
import json

from pydantic.utils import truncate
from .interface import DB
from typing import Dict, Any
from pydantic import BaseModel

class Data(BaseModel):
    id: str
    data: Dict[str,Any]

class DB_Example(DB):
    def __init__(self, path_db):
        self._path_db = path_db
        if os.path.exists(path_db):
            with open(path_db, 'r') as myfile:
                self._database = json.loads(myfile.read())
        elif os.path.exists(os.path.join(os.getcwd(),path_db)):
            path_db = os.path.join(os.getcwd(),path_db)
            with open(path_db, 'r') as myfile:
                self._database = json.loads(myfile.read())
            self._path = path_db
        else:
            raise Exception("There is not a database")
    
    def post(self,data: Data):
        self._database.update(data["id"],data['data'])

    def get_by_key(self,key):
        if key in self._database:
            return self._database[key]
        return None

    def delete_by_key(self,key):
        if key in self._database:
            self._database.pop(key)
            return True
        return None

    def __iter__(self):
        return [Data(key,self._database[key]) for key in self._database.keys()]

    def __del__(self):
        with open(self._path_db, 'w') as myfile:
            myfile.write(json.dumps(self._database))


class DB_OWN(DB):
    def post(self,data: Data):
       ...

    def get_by_key(self,key):
       ...

    def delete_by_key(self,key):
        ...

    def __iter__(self):
        ...

    def __del__(self):
        ...


def create_acess_database(path):
    return DB_Example(path)