# Template FastApi Auth

A template to a fastapi project with auth, middleware and injection depedencie


## Secure

The project offer two types of auth

1. Basic
2. JWT

The project using [users.json] as database. 

1. ## Add auth in function/endpoint

To add auth in some function/endpoint, we need add

```python
user = Depends(get_current_user)
```

as one of argument. If user is not in database, the system will return HttpException

2. ## Override Database

To overrride the Database, we need to acess main.py
and finish the DatabaseUserPersonal class
and change create_database to

```python
def create_database_user(*arg,**kwargs):
    DB_USER = DatabaseUserPersonal()
```

The arguments of create_database_user can be modify in app.py


3. ## Tests

All basic tests relate to auth are all implement, include integration test, in case to overrride database


## Database

The project provide [database.json] as database 

1. ## Add database in function/endpoint

To add auth in some function/endpoint, we need add

```python
db = Depends(get_database)
```

as one of argument. 

2. ## Overrride Database

To overrride the Database, we need to acess main.py
and finish the  class DB_Personate(DB) 
and change create_database to

```python
def create_database(*arg,**kwargs):
    DB_USER = DB_Personate()
```

The arguments of create_database_user can be modify in app.py

3. ## Tests

The test can be create in tests folders. 

## Endpoints

1. ## Create

To create new endpoints, we can create at [app.py]()
or [{{cookiecutter.struct}}.py](). 

2. ## Tests

The test can be create in tests folders. 


## Middleware

1. ## Override Middleware

To overrride the Middleware, we need to acess main.py
and finish the  class Middware_Personalite 
and change create_database to

```python
def create_middware(*arg,**kwargs):
    return Middware_Personalite()
```

The arguments of create_database_user can be modify in app.py

The method middleware_before is call before the endpoint and receive the request

The method middleware_after is call afther the endpoint and receive the response


## Configuration

The project use [configparse](). To add new configuration, modify the [settings.ini]()


