from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.utils.common import check_email_exists, is_update_data_valid
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import generate_hash
from app.models.user import User
from app.services.crud import create, get_by_id, commit_instance


def create_user(db: Session, user_data: UserCreate):
    try:
        new_user = User(**user_data.model_dump())

        # Validate fields
        if user_data.name == '' or user_data.email == '':
            raise HTTPException(422, 'Empty fields.')
        if user_data.password == '':
            raise HTTPException(422, 'Empty password.')
        if check_email_exists(user_data.email, db):
            raise HTTPException(409, 'Duplicate email.')

        new_user.password = generate_hash(user_data.password)

        return create(db, new_user)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_user_by_id(db: Session, user_id: int):
    try:
        user = get_by_id(db, User, user_id)
        return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_user(db: Session, user_id: int, user_update_data: UserUpdate):
    try:
        user = get_by_id(db, User, user_id, 'User not found')

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
            user.password = generate_hash(user_update_data.new_password)
            is_data_modified = True

        if is_data_modified:
            user.updated_at = datetime.now(timezone.utc)
            commit_instance(db, user)

        return user

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_user(db: Session, user_id: int):
    try:
        user = get_by_id(db, User, user_id, 'User not found')

        user.deleted_at = datetime.now(timezone.utc)

        return commit_instance(db, user)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))