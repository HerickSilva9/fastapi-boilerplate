from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.db_provider import get_session
from app.services import user

user_router = APIRouter()


@user_router.post('/new-user/', 
                response_model=UserResponse, 
                tags=['Usuários'],
                summary='Adicionar um novo usuário'
)
def create_user(
    new_user_data: UserCreate,
    db: Session = Depends(get_session)
):
    return user.create_user(new_user_data, db)


@user_router.get('/list-users/', 
                 response_model=list[UserResponse], 
                 tags=['Usuários'],
                 summary='Listar usuários'
)
def list_users(db: Session = Depends(get_session)):
    return user.list_users(db)


@user_router.put('/update-user/{user_id}/', 
                 response_model=UserResponse, 
                 tags=['Usuários'],
                 summary='Atualizar dados do usuário'
)
def update_user(
    user_id: int,
    user_update_data: UserUpdate,
    db: Session = Depends(get_session)
):
    return user.update_user(user_id, user_update_data, db)


@user_router.delete('/delete-user/{user_id}', 
                    response_model=UserResponse, 
                    tags=['Usuários'],
                    summary='Deletar um usuário'
)
def delete_user(user_id: int, 
                db: Session = Depends(get_session)
):
    return user.delete_user(user_id, db)