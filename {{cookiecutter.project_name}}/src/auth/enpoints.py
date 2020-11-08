import configparser
from fastapi import Depends, HTTPException, status
from .usermodel import UserView
from .database import UserDatabase

PATH_USERDATABASE = ""
USERDATABASE = UserDatabase(PATH_USERDATABASE)

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
app_security = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app_security.post("/token")
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






































