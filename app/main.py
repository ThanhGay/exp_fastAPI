from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine
from app.api.v1.router import router as api_v1_router
from app.db.models.base import BaseAuth, BaseProd
from app.middleware import RequestLoggingMiddleware, CORSMiddleware
import logging


def create_tables():
    BaseAuth.metadata.create_all(bind=engine)
    BaseProd.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_v1_router)


def add_middleware(app):
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CORSMiddleware)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        # stream=sys.stdout,   # đổi sang stdout nếu muốn
        # filename="app.log",  # hoặc ghi file thay vì console
        # filemode="a",
    )


def start_application():
    setup_logging()

    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    add_middleware(app=app)
    include_router(app=app)
    return app


app = start_application()
