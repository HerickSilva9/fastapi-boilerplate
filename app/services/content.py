from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.content import Content
from app.models.user import User
from app.schemas.content import ContentCreate, ContentUpdate
from app.utils.common import is_update_data_valid
from app.services.crud import create, get_by_id, commit_instance

content_not_found = 'Content not found'


def create_content(db: Session, content_data: ContentCreate):
    try:
        get_by_id(db, User, content_data.user_id, 'User not found')

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
        db: Session,
        content_id: int, 
        content_update_data: ContentUpdate 
):
    try:
        content = get_by_id(db, Content, content_id, content_not_found)

        is_data_modified = False

        if is_update_data_valid(content_update_data.new_title):
            content.title = content_update_data.new_title
            is_data_modified = True

        if is_update_data_valid(content_update_data.new_content):
            content.content = content_update_data.new_content
            is_data_modified = True

        if is_data_modified:
            content.updated_at = datetime.now(timezone.utc)
            commit_instance(db, content)

        return content
        
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_content(db: Session, content_id: int):
    try:
        content = get_by_id(db, Content, content_id, content_not_found)

        content.deleted_at = datetime.now(timezone.utc)
        return commit_instance(db, content)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))