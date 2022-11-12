from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import numpy as np

from check_cred import check_cred

from Test import Test
from AdminTest import AdminTest

df = pd.read_csv("../data/questions.csv")
df = df.drop(["remark"], axis = 1)
subjects = list(df["subject"].unique())

users_db = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}

admin_db = {"admin" : "4dm1N"}


api = FastAPI(
        title = "Création de QCM", 
        description = "Cette API permet de générer des QCM de 5, 10 ou 20 questions avec des filtres de sujets.",
        version = "1.0.0",
        openapi_tags= [
            {
                "name" : "Génération d'un QCM",
                "description" : "Cette requête permet de générer un QCM avec des sujets prédéfinis"
            },
            {
                "name" : "Ajout de questions",
                "description" : "Cette requête permet d'ajouter une question par un admin"
            }
        ])

security = HTTPBasic()

@api.post("/tests/new", tags = ["Génération d'un QCM"], name = "")
def new_test(test:Test, credentials : HTTPBasicCredentials = Depends(security)):
    if check_cred(users_db, credentials):
        if test.nombre not in [5,10,20]:
            raise HTTPException(400, "You can only choose 5, 10 or 20 questions")
        string = "".join(test.subjects)
        data = df.copy()
        data["is_in"] = data["subject"].apply(lambda x : x in string)
        data = data.loc[(data["is_in"]) & (data["use"]==test.use)]
        try : 
            data = data.drop(["is_in", "correct", "subject", "use"], axis = 1).sample(test.nombre).T.to_json()
        except ValueError:
            raise HTTPException(400, "Cannot create a new test of {} questions. Change your filters".format(test.nombre))
        return data

@api.post("/tests/create", tags = ["Ajout de questions"], name = "")
def new_test(test:AdminTest, credentials : HTTPBasicCredentials = Depends(security)):
    if check_cred(admin_db,credentials):
        df = pd.read_csv("../data/questions.csv", index_col = False)
        test = pd.DataFrame(pd.Series(test.dict())).T.replace({"null":np.nan})
        df = pd.concat([df, test])
        df.to_csv("../data/questions.csv", index = False)
        return {"Status":"Done"}

