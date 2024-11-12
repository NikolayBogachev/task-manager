from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter


from app.handlers import router, logger

from database.db import init_db
from database.redis import init_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()
    await init_redis()

    logger.info("Приложение успешно запущено")
    yield

    await close_redis()


app = FastAPI(title="task_manager", lifespan=lifespan)


main_api_router = APIRouter()

main_api_router.include_router(router)

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
