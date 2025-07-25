from sqlalchemy.orm import Session
from app.models.user import User


def check_email_exists(new_email: str, db: Session) -> bool:
    """
    Verifica se o novo email já existe na base de dados.

    Retorna `True` se já existir e `False` se não existir.
    """
    return db.query(User).filter(User.email == new_email).first() is not None


def is_update_data_valid(new_content) -> bool:
    """
    Retorna True se o dado para atualização for válido e False caso contrário. 
    """
    invalid_data = (None, '', 'string')
    return new_content not in invalid_data