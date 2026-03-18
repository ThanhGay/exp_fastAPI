from pydantic import BaseModel, Field, computed_field


class BaseQueryParams(BaseModel):
    """Query params dùng chung cho các API get_all (list)."""

    page: int = Field(default=1, ge=1, description="Trang (bắt đầu từ 1)")
    limit: int = Field(default=10, ge=1, le=100, description="Số bản ghi mỗi trang")
    keyword: str | None = Field(
        default=None,
        max_length=200,
        description="Từ khóa tìm kiếm (tùy chọn)",
    )

    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
