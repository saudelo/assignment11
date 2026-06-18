"""Travel Log"""
from fastapi import FastAPI
from routers import router

# Create the FastAPI application instance
app = FastAPI(
    title="Travel Log",
    description="A simple API for managing Travel records.",
    version="1.0.0"
)

app.include_router(router)