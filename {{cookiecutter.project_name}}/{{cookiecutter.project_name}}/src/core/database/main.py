
from .interface import DB
from .database import Data,DB_Example


class DB_Personate(DB):
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

  
DB_app = None

def create_database(*arg,**kwargs):
    DB_app = DB_Example(*arg)

def get_database():
    global DB_app
    return DB_app