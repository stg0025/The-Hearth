from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import create_user, get_all_sessions, get_days, get_user, verify_user, log_session

class RegisterModel(BaseModel):
    name : str
    addiction: str
    password: str

class LoginModel(BaseModel):
    name: str
    password: str

class CheckinModel(BaseModel):
    user_id: int
    emotion: str
    unmet_need: str
    relapsed: bool
    notes: str

class CravingModel(BaseModel):
    user_id: int
    emotion: str

app = FastAPI()

@app.post("/register")
def register(data: RegisterModel):
    if get_user(data.name):
        raise HTTPException(status_code=409, detail="User already exists")
    user_id = create_user(data.name, data.addiction, data.password)
    return {"message": "User registered successfully", "user_id": user_id}

@app.post("/login")
def login(data: LoginModel):
    user = verify_user(data.name, data.password)
    if user:
        return {"message": "User logged in successfully", "user_id": user[0]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/checkin")
def checkin(data: CheckinModel):
    session_id = log_session(data.user_id, data.emotion, data.unmet_need, data.relapsed, data.notes)
    return {"message": "User checked in successfully", "session_id": session_id}

@app.post("/craving")
def craving(data: CravingModel):
    craving_id = log_session(data.user_id, data.emotion, "N/A", False, "Craving session")
    return {"message": "Craving reported successfully", "craving_id": craving_id}

@app.get("/dashboard")
def dashboard(user_id: int):
    days = get_days(user_id)
    sessions = get_all_sessions(user_id)
    return {"message": "Dashboard data retrieved successfully", "days": days, "sessions": sessions}