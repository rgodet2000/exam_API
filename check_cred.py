from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def check_cred(database, cred: HTTPBasicCredentials = Depends(security)):
    username = cred.username
    password = cred.password
    try :
        database[username]
    except KeyError:
        raise HTTPException(403, "{} username not found".format(username))
    if database[username] != password:
        raise HTTPException(401, "password incorect")
    else:
        return True