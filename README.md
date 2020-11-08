# template_fastapi_auth

A template to a fastapi project with project and injection dependencie



## Secure

To add authentification in endpoint, you need add 

```
user = Depends(get_current_user)
```
 
in the argument of function