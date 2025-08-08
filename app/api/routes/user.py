from fastapi import APIRouter

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.dependencies import SessionDep
from app.services import user

router = APIRouter(prefix='/user', tags=['Usuários'])


@router.post('/new/', response_model=UserResponse)
def create_user(db: SessionDep, new_user_data: UserCreate):
    return user.create_user(db, new_user_data)


@router.get('/get/{user_id}', response_model=UserResponse)
def get_user_by_id(db: SessionDep, user_id: int):
    return user.get_user_by_id(db, user_id)


@router.put('/update/{user_id}/', response_model=UserResponse)
def update_user(db: SessionDep, user_id: int, user_update_data: UserUpdate):
    return user.update_user(db, user_id, user_update_data)


@router.delete('/delete/{user_id}', response_model=UserResponse)
def delete_user(db: SessionDep, user_id: int):
    return user.delete_user(db, user_id)