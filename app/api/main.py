from fastapi import APIRouter

from app.api.routes import user, content

api_router = APIRouter()
api_router.include_router(user.router)
api_router.include_router(content.router)