#Create (REQUIRED)	At least one POST endpoint that adds a new record
#Read (all) (REQUIRED)	At least one GET endpoint that returns all records
#Read (single) (REQUIRED)	At least one GET endpoint that returns a single record by ID
#Update (REQUIRED)	At least one PUT or PATCH endpoint that modifies an existing record
#Delete (REQUIRED)	At least one DELETE endpoint that removes a record by ID

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Base Model based on the JSON model of the data
class TravelLogBase(BaseModel):
    id: int
    username: str
    name: str
    destination: str
    start_date: date
    end_date: date
    highlights: list[str]
    created_at: datetime


# (POST) Usees the above model^ as the base to create new entry
class TravelLogCreate(TravelLogBase):
    name: str
    destination: str
    start_date: date
    end_date: date
    highlights: list[str]

# (PATCH) Partial updates and makes every attribute optional to fill
class TravelLogUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    highlights: Optional[list[str]] = None

# (GET) Outgoing data
class TravelLogResponse(TravelLogBase):
    id: int #added on id for the travel log
    username: str
    created_at: datetime

    
# Login model
class LoginInfo(BaseModel):
    username: str
    password: str

class DeleteResponse(TravelLogBase):
    username: str
    message: str
class ErrorResponse(BaseModel):
    status_code: int
    details: str