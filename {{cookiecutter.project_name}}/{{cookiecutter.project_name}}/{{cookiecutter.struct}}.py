import configparser
from fastapi import FastAPI, Depends,HTTPException,APIRouter
from .src.core.database.main import get_database
{% if cookiecutter.security != 'NO Auth'%}
from .src.core.auth.enpoints import get_current_user
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
async def check_work(user = Depends(get_current_user), db = Depends(get_database)):
    if user is None:
        raise HTTPException(
        status_code=401,
        detail="No Authorize"
    )
    return "OK" 
{% endif %}

