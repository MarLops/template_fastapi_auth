import configparser
from fastapi import FastAPI, Depends,HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .src.core.database.main import create_database, get_database
{% if cookiecutter.security != 'NO Auth'%}
from .src.core.auth.enpoints import app_security,get_current_user
{% endif %}
from .src.core.middleware.main import create_middware
from .src.core.auth.main import create_database_user
from .src.{{cookiecutter.struct}} import sub_app

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

{% if cookiecutter.struct == "router"%}
app.include_router(sub_app,tags=['{{cookiecutter.name_tag_or_subendpoint}}'])
{% else%}
app.mount('/{{cookiecutter.name_tag_or_subendpoint}}', sub_app)
{% endif %}
