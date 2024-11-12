import redis.asyncio as redis
from redis.asyncio import Redis
from config import config
from datetime import timedelta



redis_instance: Redis = None

async def get_redis() -> Redis:
    """Возвращает глобальный экземпляр Redis, если он инициализирован"""
    global redis_instance
    if not redis_instance:
        redis_instance = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=0,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_instance

async def init_redis():
    """Инициализирует подключение к Redis"""
    global redis_instance
    if not redis_instance:
        redis_instance = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=0,
            encoding="utf-8",
            decode_responses=True
        )

async def close_redis():
    """Закрывает подключение к Redis"""
    global redis_instance
    if redis_instance:
        await redis_instance.close()
        redis_instance = None

async def save_refresh_token_in_redis(username: str, refresh_token: str, expires_in: timedelta):
    """Сохраняем refresh токен в Redis с истечением срока действия"""
    redis_conn = await get_redis()
    ttl = expires_in.total_seconds()  # Время жизни токена в секундах
    await redis_conn.setex(f"refresh_token:{username}", ttl, refresh_token)

async def get_refresh_token_from_redis(username: str):
    """Получаем refresh токен из Redis"""
    redis_conn = await get_redis()
    return await redis_conn.get(f"refresh_token:{username}")

async def delete_refresh_token_from_redis(username: str):
    """Удаляем refresh токен из Redis"""
    redis_conn = await get_redis()
    await redis_conn.delete(f"refresh_token:{username}")
