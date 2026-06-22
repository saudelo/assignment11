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
@router.get("/user-auth/", tags=["Auth"], summary = "This is a test endpoint.", description = "This is a test endpoint. Requires authentication. Returns a string with the username and authentication status.")
def get_user(username: str = Depends(get_current_user)):
    return f"status: authenticated, username: {username}"

#get all user logs
@router.get("/all-travel-logs/", response_model = list[TravelLogBase], responses = {200: {"OK - All logs displayed"}}, tags=["GetAllLogs"],  summary="Get all logs.", description = "Get all logs. Intentionally public. Returns a list of Travel logs")
def get_all_logs():
    travel_logs = read_travel_logs()
    return travel_logs

#get a log by id
@router.get("/user/travel-logs/{id}", response_model = TravelLogBase,
            responses = {
                404:{"NotFound-A log with the specified ID could not be found"},
                200:{"OK - ID successfully found and log is displayed"}
            }, 
            tags=["LogByID"], summary="Gets a log by its ID, but only if it belongs to the logged in user",
              description= "Get log by ID. Intentionally public. Returns the log with the specified id.")
def log_by_id(id:int):
    travel_log = get_id_travel_log(id)
    return travel_log

#delete a log by id
@router.delete("/user/travel-logs/delete/{id}",response_model = DeleteResponse,
               responses= { 404:{"NotFound-A log with the specified ID could not be found"},
               403:{"Forbidden - User is not authorized to delete this log"},
               401:{"Unauthorized - User login error"},
               200:{"OK - ID successfully found, user authorized, and log deleted"}},
               tags=["DeleteLogByID"],  summary="Deletes a log by its unique ID" , description =  "Deletes a log with the specified ID. Uses auth to verify the log belongs to the user intending to delete it."
               " Returns a success message with the ID of the deleted log and the username if the log is found and belongs to that user. Otherwise it returns an error.")
def delete_log_by_id(id:int , username: str = Depends(get_current_user)):
    response = get_id_travel_log_delete(id,username)
    return response

@router.get("/status")
async def get_status():
    return {"status": "running", "version": "1.0.0"}

@router.post("/travel-logs", response_model=TravelLogResponse, tags=["Travel Logs"], 
             summary="Posts a travel log based on user logged in",
             description="Posts a travel log based on account logged in and uses the username along with the entered entries of name, destination, start date, end date, and highlights. ID and created at are both generated." )
def create_travel_log(travel_log: TravelLogCreate, username: str = Depends(get_current_user)):
    logs = read_travel_logs()
    next_id = 1 if not logs else max(log["id"] for log in logs) + 1

    created_at = datetime.now(UTC)

    new_log = {
        "id": next_id,
        "username": username,
        "name": travel_log.name,
        "destination": travel_log.destination,
        "start_date": str(travel_log.start_date),
        "end_date": str(travel_log.end_date),
        "highlights": travel_log.highlights,
        "created_at": created_at.isoformat()
    }

    logs.append(new_log)
    write_data(TRAVEL_LOG_FILE, logs)

    return new_log

@router.post("/user", summary="Adds a new account with username and password",
             description="Adds a new user to the database with username and password")
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

