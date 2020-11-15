import configparser
from fastapi import FastAPI, Depends,HTTPException,status
from starlette.middleware.base import BaseHTTPMiddleware
from src.database.main import create_database, get_database
{% if cookiecutter.security != 'NO Auth'%}
from src.auth.enpoints import app_security,get_current_user
{% endif %}
from src.middleware.main import create_middware
from src.auth.main import create_database_user


config = configparser.ConfigParser()
config.read('settings.ini')

app = FastAPI(title='{{cookiecutter.project_name}}',
              version='{{cookiecutter.version}}')


{% if cookiecutter.security != 'NO Auth'%}
app.include_router(app_security,prefix='',tags=['User'])
{% endif %}

app.add_middleware(BaseHTTPMiddleware,dispatch=create_middware(config))

@app.on_event("startup")
async def startup_event():
    create_database(config)
    create_database_user(config)


"""
#Example

@app.get("/{key}")
async def get_product(key: str, user = Depends(get_current_user), DB = Depends(get_database)):
    if DB is not None:
        return DB.get_by_key(key)
    raise HTTPException(
        status_code=500,
        detail="No Db available"
    )

"""