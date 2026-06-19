from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.adapter.schemas.error_schema import ErrorDetail, ErrorResponse
from app.contexts.artist.artist_exception import (
    ArtistBadRequestException,
    ArtistDuplicateNameException,
)
from app.contexts.shared.exceptions import BussinessException

EXCEPTION_STATUS_MAP: dict[type[BussinessException], int] = {
    ArtistBadRequestException: 400,
    ArtistDuplicateNameException: 409,
}


async def business_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, BussinessException):
        return await unhandled_exception_handler(request, exc)

    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
    body = ErrorResponse(
        code=exc.code,
        message=exc.message,
        details=[ErrorDetail(message=d.message, field=d.field) for d in exc.details],
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    body = ErrorResponse(
        code="INTERNAL_SERVER_ERROR",
        message="予期しないエラーが発生しました。",
    )
    return JSONResponse(status_code=500, content=body.model_dump())


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BussinessException, business_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
