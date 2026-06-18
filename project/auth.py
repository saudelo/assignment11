import secrets
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status


USERS = {
    "alice": "password123",
    "bob":   "securepass"
}

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    stored_password = USERS.get(credentials.username, "")
    # If the username does not exist, .get() returns "" so that
    # compare_digest still runs — this prevents an attacker from
    # detecting valid usernames by observing faster rejection times.

    # secrets.compare_digest() always takes the same time regardless
    # of where the two strings differ — timing measurement is useless.
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