from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.utils.common import (
    check_email_exists, get_if_exists, is_update_data_valid)
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import generate_hash
from app.models.user import User


def create_user(user_data: UserCreate, db: Session):
    try:
        new_user = User(name=user_data.name, email=user_data.email)

        # Verificar se os dados enviados são uma string vazia
        if user_data.name == '' or user_data.email == '':
            raise HTTPException(
                status_code=422, detail='Campos vazios não são válidos.'
            )

        if user_data.password == '':
            raise HTTPException(
                status_code=422, detail='Senha vazia não é permitida.'
            )

        if check_email_exists(user_data.email, db):
            raise HTTPException(
                status_code=409, 
                detail='Existe uma conta associada a este endereço de email.'
            ) 

        new_user.hash_password = generate_hash(user_data.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Atualiza o objeto com os dados do banco
        return new_user

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def list_users(db: Session):
    try:
        users = db.query(User).all()
        return users
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_user(
        user_id: int,  
        user_update_data: UserUpdate,
        db: Session
):
    try:
        user = get_if_exists(
            User, db, 'Usuário não encontrado', User.id == user_id
        )
        
        # Tratamento de erro para não permitir email duplicado
        if check_email_exists(user_update_data.new_email, db):
            raise HTTPException(
                status_code=409, 
                detail='Existe uma conta associada a este endereço de email.'
            )

        is_data_modified = False

        if is_update_data_valid(user_update_data.new_name):
            user.name = user_update_data.new_name
            is_data_modified = True

        if is_update_data_valid(user_update_data.new_email):
            user.email = user_update_data.new_email
            is_data_modified = True

        if is_update_data_valid(user_update_data.new_password):
            user.hash_password = generate_hash(user_update_data.new_password)
            is_data_modified = True

        if is_data_modified:
            user.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)  # Atualiza o objeto com os dados do banco

        return user
        
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_user(user_id: int, db: Session):
    try:
        user = get_if_exists(
            User, db, 'Usuário não encontrado', User.id == user_id
        )

        user.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

        return user
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        