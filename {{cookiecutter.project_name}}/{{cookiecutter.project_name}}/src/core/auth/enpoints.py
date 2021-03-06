import configparser
from fastapi import Depends, HTTPException,APIRouter
from pydantic import BaseModel
from .usermodel import FullUser, UserView
from .main import get_database_user


config = configparser.ConfigParser()
config.read('settings.ini')

INCLUDE_SCHEME = {{cookiecutter.enable_auth_endpoints_in_swagger}}

app_security = APIRouter()


{% if cookiecutter.security == 'Basic'%}
from fastapi.security import HTTPBasic, HTTPBasicCredentials
security = HTTPBasic()

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security),
                            database_user = Depends(get_database_user)) -> UserView:
    try:
        user = database_user.get_user(credentials.username,credentials.password)
        if user is not None:
            return user.dict()
        raise HTTPException(
            status_code=401,
            detail="User is not in Database",
            headers={"WWW-Authenticate": "Basic"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
{% else %}
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .utlis import create_token, recove_from_token

class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app_security.post("/token",response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 database_user = Depends(get_database_user)):
    user = database_user.get_user(form_data.username, form_data.password)
    if not user or user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return recove_from_token(token)
    except Exception as e:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
        raise credentials_exception
{% endif %}

@app_security.post("/user",description="Add new user",include_in_schema=INCLUDE_SCHEME)
async def add_user(new_user: FullUser, user = Depends(get_current_user),
                    database_user = Depends(get_database_user)):
    try:
        if user["permition"] == "admin":
            result = database_user.post(new_user)
            
            return result

        else:
            credentials_exception = HTTPException(
                status_code=401,
                detail="Only user with permition admin can add user")
            raise credentials_exception
    except Exception as e:
        credentials_exception = HTTPException(
            status_code=500,
            detail=str(e)
        ) 
        raise credentials_exception



@app_security.delete("/user/{username}",description="Add new user",include_in_schema=INCLUDE_SCHEME)
async def delete_user(username: str, user = Depends(get_current_user),
                    database_user = Depends(get_database_user)):
    try:
        if username == user["username"]:
            raise Exception("We cannot delete yourself")
        if user["permition"] == "admin":
            database_user.delete(username)
            return "Delete"
        else:
            credentials_exception = HTTPException(
                status_code=401,
                detail="Only user with permition admin can add user")
            raise credentials_exception
    except Exception as e:
        credentials_exception = HTTPException(
            status_code=500,
            detail=str(e)
        ) 
        raise credentials_exception


@app_security.put("/user",description="Add new user",include_in_schema=INCLUDE_SCHEME)
async def update_user(user_new: FullUser, user = Depends(get_current_user),
                    database_user = Depends(get_database_user)):
    try:
        if user["username"] == user["username"] and user["permition"] != user["permition"]:
            raise Exception("We cannot change your own permition")
        if user["permition"] == "admin":
            database_user.update(user_new)
            return "Update"
        else:
            credentials_exception = HTTPException(
                status_code=401,
                detail="Only user with permition admin can add user")
            raise credentials_exception
    except Exception as e:
        credentials_exception = HTTPException(
            status_code=500,
            detail=str(e)
        ) 
        raise credentials_exception
