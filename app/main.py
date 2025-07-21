from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.routes.content import content_router
from app.api.routes.user import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(content_router)

# origins = [""] # Lista de origens permitidas

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
