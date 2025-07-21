from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.main import api_router

app = FastAPI()

app.include_router(api_router)

# origins = [""] # Lista de origens permitidas

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
