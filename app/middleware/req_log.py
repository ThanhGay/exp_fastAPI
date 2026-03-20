import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


def _client_ip(request) -> str:
    """Lấy IP client: ưu tiên header khi đứng sau proxy."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "-"


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000

        ip = _client_ip(request)
        rid = getattr(request.state, "request_id", "-")

        logger.info(
            '\n%s | rid=%s | "%s - %s" %s %.3fms',
            ip,
            rid,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        return response
