from fastapi import APIRouter

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.dependencies import SessionDep
from app.services import user

router = APIRouter(prefix='/user', tags=['Usuários'])


@router.post('/new/', response_model=UserResponse)
def create_user(new_user_data: UserCreate, db: SessionDep):
    return user.create_user(db, new_user_data)


@router.get('/list/', response_model=list[UserResponse])
def list_users(db: SessionDep):
    return user.list_users(db)


@router.put('/update/{user_id}/', response_model=UserResponse)
def update_user(user_id: int, user_update_data: UserUpdate, db: SessionDep):
    return user.update_user(db, user_id, user_update_data)


@router.delete('/delete/{user_id}', response_model=UserResponse)
def delete_user(user_id: int, db: SessionDep):
    return user.delete_user(db, user_id)