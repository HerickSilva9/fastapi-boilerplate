"""Modelos Pydantic de conteúdo para validação de dados da API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

# Modelos Pydantic para Conteúdo
class ContentCreate(BaseModel):
    user_id: int
    title: Optional[str] = None
    new_content: str


class ContentResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str] = None
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class ContentUpdate(BaseModel):
    user_id: int
    new_title: Optional[str] = None
    new_content: Optional[str] = None