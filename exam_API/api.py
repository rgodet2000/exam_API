from fastapi import FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Header, Depends
from pydantic import BaseModel
from typing import Optional
from typing import List
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
import pandas as pd


df = pd.read_csv("questions.csv")
df = df.drop(["remark"], axis = 1)
subjects = list(df["subject"].unique())

class Test(BaseModel):
    nombre:Optional[int]=20
    subjects:Optional[List[str]]=subjects
    use:Optional[str]="Test de positionnement"


users_db = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}


admin_db = {"admin" : "mdp"}


api = FastAPI(title = "Création de test", openapi_tags= [])
security = HTTPBasic()


def check_cred(cred: HTTPBasicCredentials = Depends(security)):
    username = cred.username
    password = cred.password
    try :
        users_db[username]
    except KeyError:
        raise HTTPException(403, "{}{} sdfgh".format(username,password))
    if users_db[username] != password:
        raise HTTPException(401, "password incorect")
    else:
        return True



@api.post("/token")
def login(success : HTTPBasicCredentials = Depends(check_cred)):
    if success:
        return {"data":"L'utilisateur est bien présent"}
    else:
        return {"data":"L'utilisateur n'existe pas dans la base de données"}


@api.post("/tests/new")
def new_test(test:Test, credentials : HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if check_cred(username, password):
        string = "".join(test.subjects)
        data = df.copy()
        data["is_in"] = data["subject"].apply(lambda x : x in string)
        data = data.loc[(data["is_in"]) & (data["use"]==test.use)]
        return data.drop(["is_in", "correct", "subject", "use"], axis = 1).sample(test.nombre).T.to_json()

@api.post("/tests/create")
def new_test(test:Test, authorization=Header(None)):
    a = authorization.split(" ")[1]
    b = a.split(":")
    username, password = b[0], b[1][:-1]
    try :
        users_db[username]
    except KeyError:
        raise HTTPException(404, "User not found")

    if users_db[username] == password:
        string = "".join(test.subjects)
        data = df.copy()
        data["is_in"] = data["subject"].apply(lambda x : x in string)
        data = data.loc[(data["is_in"]) & (data["use"]==test.use)]
        return data.drop(["is_in", "correct", "subject", "use"], axis = 1).sample(test.nombre).T.to_json()
    else:
        raise HTTPException(404, "Password incorect")

@api.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}

