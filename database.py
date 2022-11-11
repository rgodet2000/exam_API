from fastapi import FastAPI
from fastapi import Header
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime

###Database###
users_db = [
    {
        'user_id': 1,
        'name': 'Alice',
        'subscription': 'free tier'
    },
    {
        'user_id': 2,
        'name': 'Bob',
        'subscription': 'premium tier'
    },
    {
        'user_id': 3,
        'name': 'Clementine',
        'subscription': 'free tier'
    }
]

###Format des données###
class User(BaseModel):
    user_id : Optional[int]
    name : str
    subscription : str

###Création de l'API###
api = FastAPI(
    title='Database', description = "gestion d'une base de données", version = "1.0.0",
    openapi_tags = [
        {
            "name" : "GET",
            "description" : "requêtes GET"
        },
        {
            "name" : 'PUT',
            "description" : "requêtes PUT"
        },
        {
            "name" : 'POST',
            "description" : "requêtes POST"
        },
        {
            "name" : 'DELETE',
            "description" : "requêtes DELETE"
        }
    ]
)

### Dictionnaire de description d'erreurs###
responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}


### Requêtes ###
@api.get('/', tags = ["GET"], name = "greets the user", responses=responses)
def get_index():
    """greets the user"""
    return {
        'greetings': 'welcome'
    }

@api.get('/users', tags = ["GET"], name = "returns info about all user", responses=responses)
def get_users():
    """returns info about all user"""
    return users_db

@api.get('/users/{userid:int}', tags = ["GET"], name = "returns info about a specific user", responses=responses)
def get_user(userid):
    """returns info about a specific user"""
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return user
    except IndexError:
        raise HTTPException(status_code = 404, detail = "Unknow user")

@api.get('/users/{userid:int}/name', tags = ["GET"], name = "returns the name of a specific user", responses=responses)
def get_user_name(userid):
    """returns the name of a specific user"""
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'name': user['name']}
    except IndexError:
        raise HTTPException(status_code = 404, detail = "Unknow user")

@api.get('/users/{userid:int}/subscription', tags = ["GET"], name = "returns the subscription of a specific user", responses=responses)
def get_user_suscription(userid):
    """returns the subscription of a specific user"""
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'subscription': user['subscription']}
    except IndexError:
        raise HTTPException(status_code = 404, detail = "Unknow user")

@api.put("/users", tags = ["PUT"], name = "creates a new user", responses=responses)
def add_user(user:User):
    """creates a new user"""
    new_id = max(users_db, key = lambda u:u.get("user_id"))["user_id"] + 1
    new_user = {"user_id":new_id, "name":user.name, "subscription": user.subscription}
    users_db.append(new_user)
    return new_user

@api.post("/users/{user_id}", tags = ["POST"], name = "modify info of a user", responses=responses)
def modif_user(user_id:int, user:User):
    """modify info of a user"""
    try:
        modif_user = list(filter(lambda x : x["user_id"]==user_id, users_db))[0]
        users_db.remove(modif_user)
        modif_user["name"] = user.name
        modif_user["subscription"] = user.subscription
        users_db.append(modif_user)
        return modif_user
    except IndexError:
        raise HTTPException(status_code = 404, detail = "Unknow user")

@api.delete("/users/{user_id}", tags = ["DELETE"], name = "deletes a user", responses=responses)
def sup_user(user_id:int):
    """deletes a user"""
    try:
        user = list(filter(lambda x : x["user_id"]==user_id, users_db))[0]
        users_db.remove(user)
        return {"user_id": user_id, "status":"Done"}
    except IndexError:
        raise HTTPException(status_code = 404, detail = "Unknow user")

###Gestion des exceptions###
###Exception personalisée###
class MyException(Exception):
    def __init__(self,
                 name : str,
                 date: str):
        self.name = name
        self.date = date

###Comment l'API gère mon exception###
@api.exception_handler(MyException)
def MyExceptionHandler(request: Request, exception: MyException):
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )
###Génération d'une erreur###
@api.get('/my_custom_exception')
def get_my_custom_exception():
    raise MyException(
      name='my error',
      date=str(datetime.datetime.now())
      )

@api.get('/headers')
def get_headers(authorization=Header(None)):
    a = authorization.split(" ")[1]
    b = a.split(":")
    return {"username":b[0], "password":b[1]}


