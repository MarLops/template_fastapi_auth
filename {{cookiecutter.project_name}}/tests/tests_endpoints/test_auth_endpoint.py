from requests.auth import HTTPBasicAuth
{% if cookiecutter.security == 'Basic'%}
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
{% endif %}
{% if cookiecutter.security == 'JWT'%}
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from {{cookiecutter.project_name}}.src.core.auth.utlis import recove_from_token
{% endif %}
from starlette.testclient import TestClient
from app import app
from {{cookiecutter.project_name}}.src.core.auth.enpoints import get_current_user
from {{cookiecutter.project_name}}.src.core.database.main import get_database
from {{cookiecutter.project_name}}.src.core.auth.usermodel import FullUser
from {{cookiecutter.project_name}}.src.core.auth.main import get_database_user

{% if cookiecutter.security != 'No Auth'%}
USER_FAKE = FullUser(username='{{cookiecutter.user}}',password='{{cookiecutter.password}}')
{% endif %}
{% if cookiecutter.security == 'Basic'%}
security = HTTPBasic()
async def override_get_user(credentials: HTTPBasicCredentials = Depends(security)):
    global USER_FAKE
    if credentials.username == USER_FAKE.username and credentials.password == USER_FAKE.password:
        return USER_FAKE
    return None

app.dependency_overrides[get_current_user] = override_get_user
{% endif %}
{% if cookiecutter.security == 'JWT'%}
class DB_Mock():
    def get_user(self,username,password):
        global USER_FAKE
        if username == USER_FAKE.username and password == USER_FAKE.password:
            return USER_FAKE
        return None

async def override_get_database_user():
    return DB_Mock()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def override_get_user(token: str = Depends(oauth2_scheme)):
    global USER_FAKE
    user = recove_from_token(token)
    if user["username"] == USER_FAKE.username and user["password"] == USER_FAKE.password:
        return USER_FAKE
    return None

app.dependency_overrides[get_current_user] = override_get_user
app.dependency_overrides[get_database_user] = override_get_database_user
{% endif %}


async def override_get_database():
    return None

app.dependency_overrides[get_database] = override_get_database

CLIENT = TestClient(app)

{% if cookiecutter.security != 'No Auth'%}
def test_get_without_auth():
    response = CLIENT.get("/")
    assert response.status_code == 401
{% endif %}


{% if cookiecutter.security == 'Basic'%}
def test_get_with_auth():
    response = CLIENT.get("/",auth=HTTPBasicAuth('{{cookiecutter.user}}','{{cookiecutter.password}}'))
    assert response.status_code == 200
{% endif %}


{% if cookiecutter.security == 'JWT'%}
def test_get_acess_token():
    response = CLIENT.post("/token",data={'username':'{{cookiecutter.user}}','password':'{{cookiecutter.password}}'})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_with_auth():
    response = CLIENT.post("/token",data={'username':'{{cookiecutter.user}}','password':'{{cookiecutter.password}}'})
    assert response.status_code == 200
    token = response.json()["access_token"]
    response = CLIENT.get("/",headers={'Authorization': 'Bearer {}'.format(token)})
    assert response.status_code == 200

{% endif %}