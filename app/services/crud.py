"""Funções de conexão com o banco de dados"""

from sqlalchemy.orm import Session
from fastapi import HTTPException


def create(db: Session, instance: object):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_by_id(db: Session, model_class, id: int, error_msg:str = 'Not found'):
    """
    Obtém um registro se existir, caso contrário, lança uma exceção. 
    
    Para exibir uma mensagem de erro personalizada, forneça o parâmetro 
    `error_msg`.
    """
    result = db.get(model_class, id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'{error_msg}')
    return result