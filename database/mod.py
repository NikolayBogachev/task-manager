from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Boolean, select,
)

from app.pydantic_models import UserOut

Base = declarative_base()


class BaseMixin(Base):
    __abstract__ = True  # Указываем, что это абстрактный класс, от него нельзя создавать таблицы

    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls):
        """Автоматически задает имя таблицы на основе имени класса в нижнем регистре"""

        return cls.__name__.lower()

    @classmethod
    async def add(cls, session: AsyncSession, **kwargs):
        """Добавить новую запись в базу данных

        Args:
            session (AsyncSession): Сессия для работы с базой данных
            **kwargs: Данные для создания новой записи

        Returns:
            instance: Созданный экземпляр модели
        """
        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        """Удалить запись по id

        Args:
            session (AsyncSession): Сессия для работы с базой данных
            id (int): Идентификатор записи для удаления

        Returns:
            bool: True если запись удалена, иначе False
        """
        result = await session.execute(select(cls).where(cls.id == id))
        instance = result.scalars().one_or_none()
        if instance:
            await session.delete(instance)
            await session.commit()
            return True
        return False

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        """Получить запись по id

        Args:
            session (AsyncSession): Сессия для работы с базой данных
            id (int): Идентификатор записи

        Returns:
            instance: Экземпляр модели, если найден, иначе None
        """
        result = await session.execute(select(cls).where(cls.id == id))
        return result.scalars().one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, id: int, **kwargs):
        """Обновить запись по id

        Args:
            session (AsyncSession): Сессия для работы с базой данных
            id (int): Идентификатор записи для обновления
            **kwargs: Данные для обновления записи

        Returns:
            instance: Обновленный экземпляр модели, если запись найдена, иначе None
        """

        instance = await cls.get_by_id(session, id)

        if instance:

            for key, value in kwargs.items():
                if value is not None:
                    setattr(instance, key, value)


            await session.commit()
            await session.refresh(instance)

            return instance

        return None


class UserInDB(BaseMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    tasks = relationship("Task", back_populates="user")

    @classmethod
    async def get_user_by_username(cls, session: AsyncSession, username: str):
        """Получить пользователя по username

        Args:
            session (AsyncSession): Сессия для работы с базой данных
            username (str): Имя пользователя

        Returns:
            instance: Пользователь с данным username, если найден, иначе None
        """
        result = await session.execute(select(cls).where(cls.username == username))
        return result.scalars().one_or_none()

    @staticmethod
    async def get_user_by_user_id(session: AsyncSession, user_id: int) -> UserOut:
        """Получить пользователя по id

                Args:
                    session (AsyncSession): Сессия для работы с базой данных
                    user_id (int): Идентификатор пользователя

                Returns:
                    user: Пользователь с данным id
                """
        result = await session.execute(select(UserInDB).filter(UserInDB.id == user_id))
        user = result.scalars().first()  # Возвращает первого найденного пользователя или None
        return user


class Task(BaseMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserInDB", back_populates="tasks")

    @classmethod
    async def get_tasks(cls, session: AsyncSession, user_id: int, status: bool = None):
        """Получить список задач для пользователя с опциональным фильтром по статусу

        Args:
            session (AsyncSession): Сессия для работы с базой данных
            user_id (int): Идентификатор пользователя
            status (bool, optional): Статус задачи (True - выполнена, False - не выполнена). Если None, фильтр не применяется

        Returns:
            list: Список задач пользователя
        """
        query = select(cls).where(cls.user_id == user_id)
        if status is not None:
            query = query.where(cls.status == status)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_task_by_id(session: AsyncSession, task_id: int):
        """Получить задачу по id

                Args:
                    session (AsyncSession): Сессия для работы с базой данных
                    task_id (int): Идентификатор задачи

                Returns:
                    task: Задача с данным id, если найдена
                """
        result = await session.execute(select(Task).filter(Task.id == task_id))
        return result.scalar()

