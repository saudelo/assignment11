#Create (REQUIRED)	At least one POST endpoint that adds a new record
#Read (all) (REQUIRED)	At least one GET endpoint that returns all records
#Read (single) (REQUIRED)	At least one GET endpoint that returns a single record by ID
#Update (REQUIRED)	At least one PUT or PATCH endpoint that modifies an existing record
#Delete (REQUIRED)	At least one DELETE endpoint that removes a record by ID

from fastapi import APIRouter


router = APIRouter()

#testing
@router.get("/")
def read_root():
    return {"message": "Welcome to the Travel log API"}

@router.get("/status")
async def get_status():
    return {"status": "running", "version": "1.0.0"}
