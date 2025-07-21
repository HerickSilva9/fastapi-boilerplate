from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.content import ContentCreate, ContentResponse, ContentUpdate
from app.core.db_provider import get_session
from app.services import content

router = APIRouter()


@router.post('/create-content/', 
                     response_model=ContentResponse, 
                     tags=['Conteúdo'],
                     summary='Criar um novo conteúdo'
)
def create_content(
    new_content_data: ContentCreate,
    db: Session = Depends(get_session)
):
    return content.create_content(new_content_data, db)


@router.get('/list-contents/',
                    response_model=list[ContentResponse],
                    tags=['Conteúdo'],
                    summary='Listar conteúdos'
)
def list_contents(db: Session = Depends(get_session)):
    return content.list_contents(db)


@router.put('/update-content/{content_id}', 
                    response_model=ContentResponse, 
                    tags=['Conteúdo'],
                    summary='Atualizar um conteúdo'
)
def update_content(content_id: int, 
                   content_update_data: ContentUpdate,
                   db: Session = Depends(get_session)
):
    return content.update_content(content_id, content_update_data, db)


@router.delete('/delete/{content_id}',
                       response_model=ContentResponse,
                       tags=['Conteúdo'],
                       summary='Deletar um conteúdo'
)
def delete_content(content_id: int, db: Session = Depends(get_session)):
    return content.delete_content(content_id, db)