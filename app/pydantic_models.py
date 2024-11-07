from datetime import date, datetime

from pydantic import BaseModel
from typing import List, Optional


class TunedModel(BaseModel):
    """
    Базовый класс для всех моделей.
    Конфигурация:
    - from_attributes: позволяет создавать модели из словарей атрибутов.
    """

    class Config:
        from_attributes = True


class User(TunedModel):
    username: str
    password: str


class UserInDB(TunedModel):
    username: str


class UserOut(TunedModel):
    id: int
    username: str


# Модели для Task
class TaskBase(TunedModel):
    title: str
    description: Optional[str] = None
    status: bool = False


class TaskCreate(TaskBase):
    user_id: int  # ID пользователя, которому принадлежит задача


class TaskUpdate(TunedModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class TaskInDB(TaskBase):
    id: int
    user_id: int


class TaskOut(TaskInDB):
    pass
