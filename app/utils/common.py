from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User


def get_if_exists(model_class, db: Session, error_message:str = None, *filters):
        """
        Obtém um registro se existir, caso contrário, lança uma exceção. 
        
        Para exibir uma mensagem de erro personalizada, forneça o parâmetro 
        `error_message`. Os filtros devem ser passados como se fossem argumentos
        parâmetros posicionais de filtro do SQLAlchemy.
        
        Parameters
        ----------
        model_class : Type[models.Base]
            A classe do modelo SQLAlchemy que representa a tabela.
        db : Session
            A sessão do banco de dados SQLAlchemy.
        error_message : str, optional
            Mensagem de erro personalizada a ser exibida se o registro não for
            encontrado. Se `None`, a mensagem padrão será usada.
        *filters : tuple
            Filtros a serem aplicados na consulta. Esses filtros devem ser
            passados como argumentos posicionais, como se fossem usados com
            o método `filter` do SQLAlchemy.

        Examples
        --------
        record = get_if_exists(
        User, db, 'Usuário não encontrado', User.id == user_id)

        record = get_if_exists(
        Content, db, None, Content.id == content_id, 
        Content.deleted_at.is_(None))
        """
        record = db.query(model_class).filter(*filters).first()

        if record is None:
            if error_message is None:
                raise HTTPException(
                    status_code=404, detail=f'Registro não encontrado.')
            else:
                raise HTTPException(status_code=404, detail=f'{error_message}')
        return record


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