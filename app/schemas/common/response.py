from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Response wrapper dùng chung toàn bộ dự án."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "code": 200,
                "message": "Success",
                "data": {},
            }
        }
    )

    success: bool = Field(default=True, description="Trạng thái xử lý")
    code: int | None = Field(default=None, description="HTTP status_code")
    message: str = Field(default="Success", description="Thông báo cho client")
    data: T | None = Field(default=None, description="Payload dữ liệu")
