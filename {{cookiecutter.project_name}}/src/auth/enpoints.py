import configparser
from fastapi import Depends, HTTPException, status,APIRouter
from pydantic import BaseModel
from .usermodel import UserView, User
from .database import UserDatabase,get_database

config = configparser.ConfigParser()
config.read('settings.ini')

PATH_USERDATABASE = config.get('DEFAULT','Path_userdatabase')
USERDATABASE = get_database(PATH_USERDATABASE)

app_security = APIRouter()


{% if cookiecutter.security == 'Basic'%}
from fastapi.security import HTTPBasic, HTTPBasicCredentials
security = HTTPBasic()

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        user = USERDATABASE.get_user(credentials.username,credentials.password)
        if user is not None:
            return user.dict()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not in Database",
            headers={"WWW-Authenticate": "Basic"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERDATABASE.get_user(form_data.username, form_data.password)
    if not user or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
        raise credentials_exception
{% endif %}

@app_security.post("/user/add",description="Add new user")
async def add_user(new_user: User, user = Depends(get_current_user)):
    try:
        if user["permition"] == "admin":
            result = USERDATABASE.post(new_user)
            if result:
                return "Add"
            return "Not Add"
        else:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only user with permition admin can add user")
            raise credentials_exception
    except Exception as e:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
        raise credentials_exception
