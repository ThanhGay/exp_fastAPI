from starlette.middleware.cors import CORSMiddleware as _CORSMiddleware
from app.core.config import settings


class MyCORSMiddleware(_CORSMiddleware):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            allow_origins=kwargs.get("allow_origins", settings.CORS_ORIGINS),
            allow_credentials=kwargs.get("allow_credentials", True),
            allow_methods=kwargs.get("allow_methods", ["*"]),
            allow_headers=kwargs.get("allow_headers", ["*"]),
        )
