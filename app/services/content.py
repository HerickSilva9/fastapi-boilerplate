from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.content import Content
from app.models.user import User
from app.schemas.content import ContentCreate, ContentUpdate
from app.utils.common import get_if_exists, is_update_data_valid
from app.services.crud import create

user_not_found = 'Usuário não encontrado'
content_not_found = 'Conteúdo não encontrado'


def create_content(content_data: ContentCreate, db: Session):
    try:
        user_id = content_data.user_id
        get_if_exists(User, db, user_not_found, User.id == user_id)

        new_content = Content(
            user_id=content_data.user_id, 
            title=content_data.title, 
            content=content_data.new_content
        )
        
        return create(db, new_content)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def list_contents(db: Session):
    try:
        contents = db.query(Content).all()
        return contents
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_content(
        content_id: int, 
        content_update_data: ContentUpdate, 
        db: Session
):
    try:
        content = get_if_exists(
            Content, db, content_not_found, Content.id == content_id
        )

        is_data_modified = False

        if is_update_data_valid(content_update_data.new_title):
            content.title = content_update_data.new_title
            is_data_modified = True

        if is_update_data_valid(content_update_data.new_content):
            content.content = content_update_data.new_content
            is_data_modified = True

        if is_data_modified:
            content.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(content)

        return content
        
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_content(content_id: int, db: Session):
    try:
        content = get_if_exists(
            Content, db, content_not_found, Content.id == content_id
        )

        content.deleted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(content)
        return content

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))