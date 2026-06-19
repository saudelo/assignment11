#Create (REQUIRED)	At least one POST endpoint that adds a new record
#Read (all) (REQUIRED)	At least one GET endpoint that returns all records
#Read (single) (REQUIRED)	At least one GET endpoint that returns a single record by ID
#Update (REQUIRED)	At least one PUT or PATCH endpoint that modifies an existing record
#Delete (REQUIRED)	At least one DELETE endpoint that removes a record by ID

from fastapi import APIRouter, Depends
from auth import get_current_user
from storage import read_travel_logs, write_data, TRAVEL_LOG_FILE, read_data, get_username_travel_log
from models import TravelLogCreate, TravelLogResponse, TravelLogBase


router = APIRouter()

#for authenticating user
@router.get("/user/", tags=["Auth"])
def get_user(username: str = Depends(get_current_user)):
    return f"status: authenticated, username: {username}"

#get all user logs
@router.get("/travel_logs/", response_model = TravelLogBase )
def get_all_logs():
    return f"{      }"


#test
@router.get("/status")
async def get_status():
    return {"status": "running", "version": "1.0.0"}

@router.post("/travel-logs")
def create_travel_log(travel_log: TravelLogCreate, username: str = Depends(get_current_user)):
    logs = read_travel_logs()

    next_id = 1 if not logs else max(log["id"] for log in logs) + 1

    new_log = {
        "id": next_id,
        "username": travel_log.username,
        "destination": travel_log.destination,
        "start_date": str(travel_log.start_date),
        "end_date": str(travel_log.end_date),
        "highlights": travel_log.highlights
    }

    logs.append(new_log)
    write_data(TRAVEL_LOG_FILE, logs)

    return new_log