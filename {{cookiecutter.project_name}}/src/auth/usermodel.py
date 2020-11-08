from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str
    email: str
    full_name:  str
    hashed_password: str
    disabled: str


class UserView(BaseModel):
    name: str
    full_name: str
    email: str


