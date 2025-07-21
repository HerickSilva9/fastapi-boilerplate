from fastapi import HTTPException
import pytest

from app.models.user import User
from app.utils import common


@pytest.fixture
def new_user(db_session):
    new_record = User(name='Test', email='my@email.com', hash_password='test')
    db_session.add(new_record)
    db_session.commit()
    db_session.refresh(new_record)
    return new_record


def test_new_user(new_user):
    assert new_user is not None
    assert new_user.id == 1


def test_check_get_if_exists_class_with_existing_user(db_session, new_user):
    record = common.get_if_exists(User, db_session, '', User.id == 1)
    
    assert record is not None
    assert isinstance(record, User)


def test_check_get_if_exists_data_with_existing_user(db_session, new_user):
    record = common.get_if_exists(User, db_session, '', User.id == 1)
    
    assert record.id == 1
    assert record.name == 'Test'
    assert record.email == 'my@email.com'
    assert record.hash_password == 'test'
    assert record.created_at is not None
    assert record.updated_at is None
    assert record.deleted_at is None


def test_check_get_if_exists_raises_exception_when_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        record = common.get_if_exists(User, db_session, '', User.id ==99999)

    assert exc_info.value.status_code == 404


def test_check_email_exists(db_session, new_user):
    # Email existente no banco de dados
    assert common.check_email_exists('my@email.com', db_session) is True

    # Email inexistente no banco de dados
    assert common.check_email_exists('another@email.com', db_session) is False


def test_is_update_data_valid_with_valid_data():
    test_str = 'name'
    test_email = 'email@email.com'

    assert common.is_update_data_valid(test_str) is True
    assert common.is_update_data_valid(test_email) is True


def test_is_update_data_valid_with_invalid_data():
    assert common.is_update_data_valid(None) is False
    assert common.is_update_data_valid('') is False
    assert common.is_update_data_valid('string') is False