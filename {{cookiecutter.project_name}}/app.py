import configparser
from fastapi import FastAPI, Depends,HTTPException,status
from src.database.database import create_acess_database, get_database
from src.auth.enpoints import get_current_user
from src.auth.enpoints import app_security
config = configparser.ConfigParser()
config.read('settings.ini')

PATH_DB = config.get("DEFAULT",'Path_db')

app = FastAPI(title='{{cookiecutter.project_name}}',
              version='{{cookiecutter.version}}')


app.include_router(app_security,prefix='',tags=['User'])


@app.on_event("startup")
async def startup_event():
    create_acess_database(PATH_DB)

"""
#Example

@app.get("/{key}")
async def get_product(key: str, user = Depends(get_current_user), DB = Depends(get_database)):
    if DB is not None:
        return DB.get_by_key(key)
    raise HTTPException(
        status_code=status.HTTP_500_UNAUTHORIZED,
        detail="No Db available"
    )

"""