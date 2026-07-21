from fastapi import FastAPI

app = FastAPI()

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