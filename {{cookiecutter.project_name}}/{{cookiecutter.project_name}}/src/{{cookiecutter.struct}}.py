import configparser
from fastapi import FastAPI, Depends,HTTPException,APIRouter
from .core.database.main import get_database
{% if cookiecutter.security != 'NO Auth'%}
from .core.auth.enpoints import get_current_user
{% endif %}


config = configparser.ConfigParser()
config.read('settings.ini')

{% if cookiecutter.struct == 'router'%}
sub_app = APIRouter()
{% else %}
sub_app = FastAPI()
{% endif %}

{% if cookiecutter.security != 'NO Auth'%}
@sub_app.get("/")
async def check_work(user = Depends(get_current_user)):
    return "OK" 
{% endif %}

"""
#Example to get database and user name

@sub_app.get("/{key}")
async def get_product(key: str, user = Depends(get_current_user), DB = Depends(get_database)):
    if DB is not None:
        return DB.get_by_key(key)
    raise HTTPException(
        status_code=500,
        detail="No Db available"
    )

"""