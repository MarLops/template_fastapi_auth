from requests.auth import HTTPBasicAuth
from starlette.testclient import TestClient
from app import app



{% if cookiecutter.security != 'No Auth'%}
def test_get_without_auth():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 401
{% endif %}

{% if cookiecutter.security == 'Basic'%}
def test_get_with_auth():
    with TestClient(app) as client:
        response = client.get("/",auth=HTTPBasicAuth('{{cookiecutter.user}}','{{cookiecutter.password}}'))
        assert response.status_code == 200

{% endif %}


{% if cookiecutter.security == 'JWT'%}
def test_get_acess_token():
    with TestClient(app) as client:
        response = client.post("/token",data={"username":'{{cookiecutter.user}}',"password":'{{cookiecutter.password}}'})
        assert response.status_code == 200
        assert "access_token" in response.json()


def test_get_with_auth():
    with TestClient(app) as client:
        response = client.post("/token",data={"username":'{{cookiecutter.user}}',"password":'{{cookiecutter.password}}'})
        assert response.status_code == 200
        token = response.json()["access_token"]
        response = client.get("/",headers={'Authorization': 'Bearer {}'.format(token)})
        assert response.status_code == 200

{% endif %}