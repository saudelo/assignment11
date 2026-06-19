#Create (REQUIRED)	At least one POST endpoint that adds a new record
#Read (all) (REQUIRED)	At least one GET endpoint that returns all records
#Read (single) (REQUIRED)	At least one GET endpoint that returns a single record by ID
#Update (REQUIRED)	At least one PUT or PATCH endpoint that modifies an existing record
#Delete (REQUIRED)	At least one DELETE endpoint that removes a record by ID

from fastapi import APIRouter, Depends
from auth import get_current_user

FILE_PATH = "project/data/travel_log.json"
router = APIRouter()

#testing
@router.get("/user/", tags=["Auth"])
def get_user(username: str = Depends(get_current_user)):
    return {
        "username" : username,
        "message": f"Hello {username}, you are authenticated."}

@router.get("/status")
async def get_status():
    return {"status": "running", "version": "1.0.0"}
