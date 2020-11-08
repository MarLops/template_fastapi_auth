import configparser
from datetime import datetime, timedelta
from jose import JWTError, jwt
from .usermodel import UserView

SECRET_KEY = ""
ALGORITHM = ""
ACCESS_TOKEN_EXPIRE_MINUTES = ""

def create_token(user: UserView):
    access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = user.dict()
    to_encode.update({"exp":access_token_expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])
    return encoded_jwt


def recove_from_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


