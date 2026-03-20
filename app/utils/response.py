from typing import TypeVar

from app.schemas.common.response import ApiResponse

T = TypeVar("T")


def ok(
    data: T | None = None,
    *,
    message: str = "Success",
    code: int | None = None,
) -> ApiResponse[T]:
    return ApiResponse(success=True, code=code, message=message, data=data)


def err(
    data: T | None = None,
    *,
    message: str = "Error",
    code: int | None = None,
) -> ApiResponse[T]:
    return ApiResponse(success=False, code=code, message=message, data=data)
