import secrets
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from storage import read_data,write_data

USERS_PATH = "project/data/login_info.json"

security = HTTPBasic()



def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    user_info =  read_data(USERS_PATH)
    stored_password = user_info.get(credentials.username, "")
    # If the username does not exist, .get() returns "" 
   
    # encode("utf-8") is required because compare_digest expects bytes.
    password_correct = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        stored_password.encode("utf-8")
    )

    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"}
        )

    return credentials.username