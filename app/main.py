from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine
from app.api.v1.router import router as api_v1_router
from app.db.models.base import BaseAuth, BaseProd


def create_tables():
    BaseAuth.metadata.create_all(bind=engine)
    BaseProd.metadata.create_all(bind=engine)


def include_router(app):   
	app.include_router(api_v1_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app

app = start_application()
