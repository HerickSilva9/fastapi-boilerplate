from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
        )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'detail': 'Internal server error.'},
        )