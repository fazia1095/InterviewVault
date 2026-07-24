from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import questions as questions_router


app = FastAPI(
    title="InterviewVault API",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Connect Questions router
app.include_router(questions_router.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to InterviewVault"
    }


@app.get("/about")
def about():
    return {
        "project": "InterviewVault",
        "version": "1.0",
        "developer": "Ibu"
    }