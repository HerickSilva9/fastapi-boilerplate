from fastapi import APIRouter

from app.schemas.content import ContentCreate, ContentResponse, ContentUpdate
from app.api.dependencies import SessionDep
from app.services import content

router = APIRouter(prefix='/content', tags=['Conteúdo'])


@router.post('/create/', response_model=ContentResponse)
def create_content(db: SessionDep, new_content_data: ContentCreate):
    return content.create_content(db, new_content_data)


@router.get('/get/{content_id}', response_model=ContentResponse)
def get_content_by_id(db: SessionDep, content_id: int):
    return content.get_content_by_id(db, content_id)


@router.put('/update/{content_id}', response_model=ContentResponse)
def update_content(
        db: SessionDep, content_id: int, content_update_data: ContentUpdate
        ):
    return content.update_content(db, content_id, content_update_data)


@router.delete('/delete/{content_id}', response_model=ContentResponse)
def delete_content(db: SessionDep, content_id: int):
    return content.delete_content(db, content_id)