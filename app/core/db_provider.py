from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.models import Base
from app.models import user, content # force import of models to create tables
from app.core import settings

# Create engine
engine = create_engine(settings.DATABASE_URL, echo=False)

Base.metadata.create_all(engine)  # Cria as tabelas se não existirem

SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()