from fastapi import APIRouter

from app.schemas.content import ContentCreate, ContentResponse, ContentUpdate
from app.api.dependencies import SessionDep
from app.services import content

router = APIRouter()


@router.post('/create-content/', 
                     response_model=ContentResponse, 
                     tags=['Conteúdo'],
                     summary='Criar um novo conteúdo'
)
def create_content(
    new_content_data: ContentCreate,
    db: SessionDep
):
    return content.create_content(new_content_data, db)


@router.get('/list-contents/',
                    response_model=list[ContentResponse],
                    tags=['Conteúdo'],
                    summary='Listar conteúdos'
)
def list_contents(db: SessionDep):
    return content.list_contents(db)


@router.put('/update-content/{content_id}', 
                    response_model=ContentResponse, 
                    tags=['Conteúdo'],
                    summary='Atualizar um conteúdo'
)
def update_content(content_id: int, 
                   content_update_data: ContentUpdate,
                   db: SessionDep
):
    return content.update_content(content_id, content_update_data, db)


@router.delete('/delete/{content_id}',
                       response_model=ContentResponse,
                       tags=['Conteúdo'],
                       summary='Deletar um conteúdo'
)
def delete_content(content_id: int, db: SessionDep):
    return content.delete_content(content_id, db)