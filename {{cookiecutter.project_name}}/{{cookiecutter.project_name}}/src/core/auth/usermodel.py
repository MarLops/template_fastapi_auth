from pydantic import BaseModel


class UserView(BaseModel):
    username: str
    full_name: str = None
    email: str = None
    permition: str = None




class FullUser(UserView):
    password: str


