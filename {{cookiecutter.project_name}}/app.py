import configparser
from fastapi import FastAPI, Depends,HTTPException,status
from .src.database.own_database import DB_Example
from .src.database.utils import create_acess_database
from .src.auth.enpoints import get_current_user

PATH_DB = ""

app = FastAPI(title={{cookiecutter.project_name}},
              version={{cookiecutter.version}})


{% if cokkiecutter.security == 'JWT' %}
from .src.auth.enpoints import app_security

app.mount('/auth',app_security)
{% endif %}

DB = None

@app.on_event("startup")
async def startup_event():
    global DB
    DB = create_acess_database(PATH_DB)

"""
Example

@app.get("/{key}")
async def get_product(key, str: user = Dependes(get_current_user)):
    if DB is not None:
        return DB.get_by_key(key)
    raise HTTPException(
        status_code=status.HTTP_500_UNAUTHORIZED,
        detail="No Db available"
    )

"""