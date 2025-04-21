from fastapi import FastAPI, HTTPException
from app.database import database
from app.auth import create_user
from app.schemas import UserCreate, UserOut
from app.schemas import UserLogin, Token
from app.auth import authenticate_user
from fastapi.responses import JSONResponse
from fastapi import Depends
from app.auth import get_current_user

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    return await create_user(user)

@app.post("/login")
async def login(credentials: UserLogin):
    token_data = await authenticate_user(credentials)
    response = JSONResponse(content={"message": "Успешный вход"})
    response.set_cookie(
        key="access_token",
        value=token_data["access_token"],
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return response

@app.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

@app.get("/ping")
async def ping():
    return {"message": "pong"}