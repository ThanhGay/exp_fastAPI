from typing import Iterable, Callable

from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.security import decode_token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        exclude_paths: Iterable[str] | None = None,
    ):
        super().__init__(app)
        self.exclude_paths = set(exclude_paths or [])

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path

        # Bỏ qua các path public (docs, login, v.v.)
        if any(path.startswith(p) for p in self.exclude_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split(" ", 1)[1].strip()
        payload = decode_token(token)

        if not payload or "sub" not in payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Gắn user_id vào request.state để handler có thể dùng nếu muốn
        request.state.user_id = int(payload["sub"])

        return await call_next(request)

