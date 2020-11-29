from .database import DB_Example


class DB():
    ...


DB_app = None


{% if cookiecutter.enable_default_database == "True"%}
def create_database(*arg,**kwargs):
    global DB_app
    DB_app = DB_Example(*arg)
{% else%}
def create_database(*arg,**kwargs):
    global DB_app
    DB_app = None

{% endif%}

def get_database():
    global DB_app
    return DB_app