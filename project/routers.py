#Create (REQUIRED)	At least one POST endpoint that adds a new record
#Read (all) (REQUIRED)	At least one GET endpoint that returns all records
#Read (single) (REQUIRED)	At least one GET endpoint that returns a single record by ID
#Update (REQUIRED)	At least one PUT or PATCH endpoint that modifies an existing record
#Delete (REQUIRED)	At least one DELETE endpoint that removes a record by ID

from fastapi import APIRouter, Depends,HTTPException
from auth import get_current_user
from storage import LOGIN_FILE, TRAVEL_LOG_FILE, read_travel_logs, write_data, read_login_info,get_id_travel_log,get_id_travel_log_delete
from models import TravelLogCreate, TravelLogResponse, TravelLogBase, LoginInfo, DeleteResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, UTC



security = HTTPBasic()

router = APIRouter()

#for authenticating user
@router.get("/user-auth/", tags=["Auth"], summary = "This is a test endpoint.")
def get_user(username: str = Depends(get_current_user)):
    """This is a test endpoint. Requires authentication. Returns a string with the username and authentication status."""
    return f"status: authenticated, username: {username}"

#get all user logs
@router.get("/all-travel-logs/", response_model = list[TravelLogBase], status_code=200, tags=["GetAllLogs"],  summary="Get all logs.")
def get_all_logs():
    """Get all logs. Intentionally public. Returns a list of Travel logs"""
    travel_logs = read_travel_logs()
    return travel_logs

#get a log by id
@router.get("/user/travel-logs/{id}", response_model = TravelLogBase, tags=["LogByID"], summary="Gets a log by its ID, but only if it belongs to the logged in user" )
def log_by_id(id:int):
    """Get log by id. Intentionally public. Returns the log with the specified id."""
    travel_log = get_id_travel_log(id)
    return travel_log

#delete a log by id
@router.get("/user/travel-logs/delete/{id}",response_model = DeleteResponse, tags=["DeleteLogByID"],  summary="Deletes a log by its unique ID" )
def delete_log_by_id(id:int , username: str = Depends(get_current_user)):
    """Deletes a log with the specified ID. Uses auth to verify the log belongs to the user. Returns a success message with the ID of the deleted log and the username."""
    response = get_id_travel_log_delete(id,username)
    return response

@router.get("/status")
async def get_status():
    return {"status": "running", "version": "1.0.0"}

@router.post("/travel-logs", response_model=TravelLogResponse, tags=["Travel Logs"])
def create_travel_log(travel_log: TravelLogCreate, username: str = Depends(get_current_user)):
    logs = read_travel_logs()

    next_id = 1 if not logs else max(log["id"] for log in logs) + 1

    created_at = datetime.now(UTC).strftime("%Y-%m-%d at %I:%M %p UTC")

    new_log = {
        "id": next_id,
        "username": username,
        "name": travel_log.name,
        "destination": travel_log.destination,
        "start_date": str(travel_log.start_date),
        "end_date": str(travel_log.end_date),
        "highlights": travel_log.highlights,
        "created_at": created_at
    }

    logs.append(new_log)
    write_data(TRAVEL_LOG_FILE, logs)

    return new_log

@router.post("/user")
def create_user_info(user: LoginInfo):
    users = read_login_info()

    new_user = {
        "username": user.username,
        "password": user.password
    }

    users.append(new_user)
    write_data(LOGIN_FILE, users)

    return new_user

@router.patch("/travel-log/{id}")
def patch_travel_log():
    return

