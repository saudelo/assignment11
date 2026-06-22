import secrets
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from storage import read_login_info



security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    print("AUTH FUNCTION CALLED")
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Missing credentials",
            headers={"WWW-Authenticate": "Basic"}
        )

    users_list =  read_login_info()
    this_user = next((u for u in users_list if u["username"] == credentials.username), None)
   

    if this_user:
        stored_password = this_user.get("password", None)
        password_correct = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        stored_password.encode("utf-8")
        )
        if password_correct:
            return credentials.username
        else:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Basic"}
        )
         
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username",
        headers={"WWW-Authenticate": "Basic"}
        )
         

 