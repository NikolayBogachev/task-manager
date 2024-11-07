import sys
from typing import List

from fastapi.params import Body
from loguru import logger

from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from starlette.responses import JSONResponse

from database.db import AsyncSession, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from app.pydantic_models import User

from app.auth import AuthService, oauth2_scheme
from config import config
from database.models import UserInDB

logger.remove()  # Удалите все существующие обработчики
logger.add(sys.stdout, level="INFO", format="{time} {level} {message}", backtrace=True, diagnose=True)


router = APIRouter()


@router.post("/auth/register")
async def register_user(user: User, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.

    **Параметры**:
    - `user` (User): Объект пользователя, содержащий имя пользователя и пароль.
    - `db` (AsyncSession): Асинхронная сессия базы данных, предоставляемая через Depends.

    **Возвращает**:
    - `access_token` (str): Токен доступа для зарегистрированного пользователя.
    - `token_type` (str): Тип токена (bearer).

    **Ошибки**:
    - 400: Если пользователь с указанным именем уже зарегистрирован.
    """
    # Проверка существования пользователя с таким именем
    db_user = await UserInDB.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Хешируем пароль и сохраняем пользователя в БД
    hashed_password = AuthService.get_password_hash(user.password)
    await UserInDB.add_user(db, user.username, hashed_password)

    # Создаем токен и возвращаем его
    access_token = AuthService.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Авторизация пользователя и получение токена доступа.
    """
    # Получаем пользователя по имени
    user = await UserInDB.get_user_by_username(db, form_data.username)

    # Если пользователь не найден
    if not user or not AuthService.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерация токенов
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(days=7)
    refresh_token = AuthService.create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/auth/refresh")
async def refresh_access_token(refresh_token: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)):
    """
    Обновление токенов с использованием refresh токена.
    """
    # Декодируем refresh токен
    payload = AuthService.decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user = await UserInDB.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Создание новых токенов
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(data={"sub": username}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=7)
    new_refresh_token = AuthService.create_refresh_token(data={"sub": username}, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
