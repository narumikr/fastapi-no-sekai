from pydantic import BaseModel


class ErrorDetail(BaseModel):
    message: str
    field: str | None = None


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = []
