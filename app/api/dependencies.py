from typing import Annotated

from app.core.db_provider import get_session
from sqlalchemy.orm import Session
from fastapi import Depends

SessionDep = Annotated[Session, Depends(get_session)]