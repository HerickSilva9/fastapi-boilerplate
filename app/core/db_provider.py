from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.models import Base
from app.models import user, content # force import of models to create tables

# Database URL
DATABASE_URL = f'sqlite:///app/core/data.db'

# Criar engine (banco SQLite)
engine = create_engine(DATABASE_URL, echo=False)

Base.metadata.create_all(engine)  # Cria as tabelas se não existirem

SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()