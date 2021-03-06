import configparser
from fastapi import FastAPI, Depends,HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from {{cookiecutter.project_name}}.src.core.database.main import create_database, get_database
{% if cookiecutter.security != 'NO Auth'%}
from {{cookiecutter.project_name}}.src.core.auth.enpoints import app_security,get_current_user
{% endif %}
from {{cookiecutter.project_name}}.src.core.middleware.main import create_middware
from {{cookiecutter.project_name}}.src.core.auth.main import create_database_user
from {{cookiecutter.project_name}}.{{cookiecutter.struct}} import sub_app

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
    path_user_db = config.get('DEFAULT','Path_userdatabase')
    create_database_user(path_user_db)
    path = config.get("DEFAULT",'Path_db')
    create_database(path)

{% if cookiecutter.struct == "router"%}
app.include_router(sub_app,tags=['{{cookiecutter.name_tag_or_subendpoint}}'])
{% else%}
app.mount('/{{cookiecutter.name_tag_or_subendpoint}}', sub_app)
{% endif %}
