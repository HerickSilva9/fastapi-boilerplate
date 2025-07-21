"""Modelos Pydantic de usuário para validação de dados da API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Modelos Pydantic para Usuários
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    # Atualizado para usar ConfigDict
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    new_name: Optional[str] = None
    new_email: Optional[str] = None
    new_password: Optional[str] = None