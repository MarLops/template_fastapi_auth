# Template FastApi Auth

A template to a fastapi'project with auth, middleware and dependency injection


## How to use

To create a project, you need install cookicutter

```python
pip install cookiecutter
```

Next, run the command

```python
cookiecutter https://github.com/MarLops/template_fastapi_auth.git
```

## Secure

The project offer two types of auth

1. Basic
2. JWT

The project using [users.json]({{cookiecutter.project_name}}/{{cookiecutter.project_name}}/src/core/auth/users.json) as Users'database, but this can modify.

1. ## Add auth in function/endpoint

To add auth in some function/endpoint, you need add

```python
user = Depends(get_current_user)
```

as one of argument. If user is not in database, the variable "user" will be None

2. ## Override Database

To overrride the database, you need to acess [main.py]({{cookiecutter.project_name}}/{{cookiecutter.project_name}}/src/core/auth/main.py)
and complete the DatabaseUserPersonal class

After you complete, we will need change create_database_user in same file


```python
def create_database_user(*arg,**kwargs):
    DB_USER = DatabaseUserPersonal()
```

The arguments of create_database_user can be modify in [app.py]({{cookiecutter.project_name}}/app.py) 


3. ## Tests

There are tests 
1. [unit test]({{cookiecutter.project_name}}/tests/test_unit/test_auth_db.py)
2. [endpoints]({{cookiecutter.project_name}}/tests/tests_endpoints/test_auth_endpoint.py)
3. [integration]({{cookiecutter.project_name}}/tests/tests_integration/test_auth.py)


## Database

The project can providence a [database]({{cookiecutter.project_name}}/{{cookiecutter.project_name}}/src/core/database/database.json) 

1. ## Overrride Database

To overrride the Database, you need to acess [main.py]({{cookiecutter.project_name}}/{{cookiecutter.project_name}}/src/core/database/main.py)
and complete the DB class

After you complete, you will need change create_database  in same file

```python
def create_database(*arg,**kwargs):
    DB_app = DB(*arg,**kwargs)
```

The arguments of create_database can be modify in [app.py]({{cookiecutter.project_name}}/app.py)


2. ## Add database in function/endpoint

To add database in some function/endpoint, you need add

```python
db = Depends(get_database)
```

as one of argument. 

3. ## Tests

The test can be create in tests folders. 

1. [unit]({{cookiecutter.project_name}}/tests/test_unit)
2. [endpoint]({{cookiecutter.project_name}}/tests/tests_endpoints)
3. [integration]({{cookiecutter.project_name}}/tests/tests_integration)

## Endpoints

1. ## Create

To create new endpoints, you can 
1. Create at [app.py]({{cookiecutter.project_name}}/app.py)
2. Create at [{{cookiecutter.struct}}.py]({{cookiecutter.project_name}}/{{cookiecutter.project_name}}/{{cookiecutter.struct}}.py)
3. Create new file and mount in [app.py]({{cookiecutter.project_name}}/app.py)



## Middleware

1. ## Override Middleware

To overrride the Middleware, you need to acess [main.py]({{cookiecutter.project_name}}/{{cookiecutter.project_name}}/src/core/middleware/main.py)
and complete the Middware_Personalite class

After you complete, you will need change create_middware  in same file

```python
def create_middware(*arg,**kwargs):
    return Middware_Personalite()
```

The arguments of create_middware can be modify in [app.py]({{cookiecutter.project_name}}/app.py)

The method middleware_before is call before the endpoint receive the request

The method middleware_after is call afther the endpoint receive the response


## Configuration

The project use configparse. To add new configuration, modify  [settings.ini file]({{cookiecutter.project_name}}/settings.ini) .



