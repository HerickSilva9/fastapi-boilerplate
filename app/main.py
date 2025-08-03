from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.main import api_router
from app.core import settings
from app.exceptions.handlers import (
    http_exception_handler, generic_exception_handler
)

app = FastAPI()

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)