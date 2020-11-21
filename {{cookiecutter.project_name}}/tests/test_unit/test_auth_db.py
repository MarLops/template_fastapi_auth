import pytest
from {{cookiecutter.project_name}}.src.core.auth.main import create_database_user,get_database_user
from {{cookiecutter.project_name}}.src.core.auth.interface import DBUser
from {{cookiecutter.project_name}}.src.core.auth.usermodel import UserView, FullUser


def test_create_db():
    create_database_user("any path")
    db = get_database_user()
    assert issubclass(type(db),DBUser)


def test_get_user():
    create_database_user("any path")
    db = get_database_user()
    user = db.get_user(name="test_user",password="test")
    assert user is None


def test_add_user_error():
    with pytest.raises(ValueError):
        create_database_user("any path")
        db = get_database_user()
        user = db.post(FullUser())
        
def test_add_user():
    create_database_user("any path")
    db = get_database_user()
    new_user = FullUser(username="test",password="test")
    db.post(new_user)
    user = db.get_user(name='test',password='test')
    assert user.username == new_user.username 
