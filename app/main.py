from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.main import api_router
from app.core import settings

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)