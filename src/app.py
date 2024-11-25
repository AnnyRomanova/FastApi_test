import uvicorn
from contextlib import asynccontextmanager
import logging.config

from fastapi import FastAPI

import controllers.post_controller as post_module
from api.posts import router as post_router
from core.settings import get_settings
from models.database import posts

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Actions before launching the application")
    post_module.controller = post_module.PostController(posts)
    yield

    logger.info("Actions after launching the application")

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(post_router, prefix="/posts", tags=["posts"])


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_config="core/logging.yaml")
