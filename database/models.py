from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Boolean, select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserInDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор пользователя
    username = Column(String, unique=True, index=True)  # Уникальное имя пользователя
    hashed_password = Column(String)  # Хеш пароля

    tasks = relationship("Task", back_populates="user")  # Связь с таблицей задач

    @classmethod
    async def add_user(cls, session: AsyncSession, username: str, hashed_password: str):
        """Добавить нового пользователя"""
        new_user = cls(username=username, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def delete_user(cls, session: AsyncSession, username: str):
        """Удалить пользователя по username"""
        result = await session.execute(select(cls).where(username == cls.username))
        user = result.scalars().one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False

    @classmethod
    async def get_user_by_username(cls, session: AsyncSession, username: str):
        """Получить пользователя по username"""
        result = await session.execute(select(cls).where(username == cls.username))
        user = result.scalars().one_or_none()
        return user


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор задачи
    title = Column(String, index=True)  # Название задачи
    description = Column(String)  # Описание задачи
    status = Column(Boolean, default=False)  # Статус задачи (выполнена или нет)
    user_id = Column(Integer, ForeignKey("users.id"))  # Внешний ключ, ссылается на таблицу users

    user = relationship("UserInDB", back_populates="tasks")  # Связь с таблицей пользователей

    @classmethod
    async def create_task(cls, session: AsyncSession, title: str, description: str, status: bool, user_id: int):
        """Создать новую задачу"""
        new_task = cls(title=title, description=description, status=status, user_id=user_id)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return new_task

    @classmethod
    async def update_task(cls, session: AsyncSession, task_id: int, title: str = None, description: str = None,
                          status: bool = None):
        """Обновить задачу по id"""
        result = await session.execute(select(cls).where(task_id == cls.id))
        task = result.scalars().one_or_none()
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if status is not None:
                task.status = status
            await session.commit()
            await session.refresh(task)
            return task
        return None

    @classmethod
    async def delete_task(cls, session: AsyncSession, task_id: int):
        """Удалить задачу по id"""
        result = await session.execute(select(cls).where(task_id == cls.id))
        task = result.scalars().one_or_none()
        if task:
            await session.delete(task)
            await session.commit()
            return True
        return False

    @classmethod
    async def get_tasks(cls, session: AsyncSession, user_id: int, status: bool = None):
        """Получить список задач для пользователя с опциональным фильтром по статусу"""
        query = select(cls).where(user_id == cls.user_id)
        if status is not None:
            query = query.where(status == cls.status)
        result = await session.execute(query)
        tasks = result.scalars().all()
        return tasks

