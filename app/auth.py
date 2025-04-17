from app.database import database
from app.models import User
from app.schemas import UserCreate
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from app.schemas import UserLogin
from sqlalchemy import select
from dotenv import load_dotenv
import os
from fastapi import Request, HTTPException

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

async def create_user(user: UserCreate):
    hashed_password = bcrypt.hash(user.password)
    query = users.insert().values(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    user_id = await database.execute(query)
    return {**user.dict(), "id": user_id}

def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(credentials: UserLogin):
    user = await database.fetch_one(select(User).where(User.email == credentials.email))

    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    if not bcrypt.verify(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    token = create_jwt_token({"sub": str(user["id"])})
    return {"access_token": token, "token_type": "bearer"}

# Проверяем токен
async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Токен не предоставлен")

    try:
        # Проверка токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Токен недействителен")

        # Извлекаем пользователя из базы
        query = users.select().where(users.c.id == user_id)
        user = await database.fetch_one(query)
        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь не найден")

        return user

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Ошибка токена")