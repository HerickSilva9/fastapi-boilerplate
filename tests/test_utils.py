from fastapi import HTTPException
import pytest

from app.models.user import User
from app.services.crud import get_by_id
from app.utils import common


@pytest.fixture
def new_user(db_session):
    new_record = User(name='Test', email='my@email.com', password='test')
    db_session.add(new_record)
    db_session.commit()
    db_session.refresh(new_record)
    return new_record


def test_new_user(new_user):
    assert new_user is not None
    assert new_user.id == 1


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