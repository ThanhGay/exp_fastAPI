import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine
from app.api.v1.router import router as api_v1_router
from app.db.models.base import BaseAuth, BaseProd, BaseOrd
from app.middleware import (
    RequestLoggingMiddleware,
    RequestIdMiddleware,
)
from app.schemas.common.response import ApiResponse


def create_tables():
    BaseAuth.metadata.create_all(bind=engine)
    BaseProd.metadata.create_all(bind=engine)
    BaseOrd.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_v1_router)


def add_middleware(app):
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        # stream=sys.stdout,   # đổi sang stdout nếu muốn
        # filename="app.log",  # hoặc ghi file thay vì console
        # filemode="a",
    )
    # return logging.getLogger(__name__)


def config_exception_handler(app):
    # handle loi http 4xx
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        response = ApiResponse(
            success=False, code=exc.status_code, message=exc.detail, data=None
        )

        return JSONResponse(status_code=200, content=response.model_dump())

    # handle loi server 5xx
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        response = ApiResponse(
            success=False, code=500, message="Internal Server Error", data=None
        )

        return JSONResponse(status_code=200, content=response.model_dump())


def start_application():
    setup_logging()

    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    add_middleware(app=app)
    include_router(app=app)
    config_exception_handler(app=app)
    return app


app = start_application()
