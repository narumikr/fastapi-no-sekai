import logging
from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from app.adapter.schemas.error_schema import ErrorDetail, ErrorResponse
from app.contexts.artist.artist_exception import (
    ArtistBadRequestException,
    ArtistDuplicateNameException,
)
from app.contexts.shared.exceptions import BussinessException

logger = logging.getLogger(__name__)

EXCEPTION_STATUS_MAP: dict[type[BussinessException], int] = {
    ArtistBadRequestException: 400,
    ArtistDuplicateNameException: 409,
}


async def business_exception_handler(
    request: Request, exc: BussinessException
) -> JSONResponse:
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
    logger.warning(
        "業務例外を捕捉しました: %s %s status=%d code=%s message=%s",
        request.method,
        request.url.path,
        status_code,
        exc.code,
        exc.message,
    )
    body = ErrorResponse(
        code=exc.code,
        message=exc.message,
        details=[ErrorDetail(message=d.message, field=d.field) for d in exc.details],
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "予期しない例外が発生しました: %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    body = ErrorResponse(
        code="INTERNAL_SERVER_ERROR",
        message="予期しないエラーが発生しました。",
    )
    return JSONResponse(status_code=500, content=body.model_dump())


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        BussinessException,
        cast(ExceptionHandler, business_exception_handler),
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)
