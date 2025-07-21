from datetime import datetime

from pydantic import ValidationError
import pytest

from app.schemas.user import UserCreate, UserResponse, UserUpdate

@pytest.fixture
def user_create():
    user = UserCreate(
        name='Test User', email='testuser@email.com', password='mypassword'
        )
    return user


@pytest.fixture
def user_response():
    user = UserResponse(
        id=15, name='Test User', email='testuser@email.com', 
        created_at=datetime(2025, 7, 9, 18, 11, 31, 114597), 
        updated_at=datetime(2025, 7, 9, 18, 11, 31, 114597), 
        deleted_at=datetime(2025, 7, 9, 18, 11, 31, 114597)
    )
    return user


@pytest.fixture
def user_update():
    user = UserUpdate(
        new_name='Test User', new_email='testuser@email.com', 
        new_password='mynewpassword'
    )
    return user


def test_schema_user_create_success(user_create):
    assert isinstance(user_create, UserCreate)
    assert user_create.name == 'Test User'
    assert user_create.email == 'testuser@email.com'
    assert user_create.password == 'mypassword'


def test_user_create_invalid_data():
    with pytest.raises(ValidationError):
        user = UserCreate()


def test_schema_user_response_success(user_response):
    assert user_response.id == 15
    assert user_response.name == 'Test User'
    assert user_response.email == 'testuser@email.com'
    assert user_response.updated_at == datetime(2025, 7, 9, 18, 11, 31, 114597)
    assert user_response.deleted_at == datetime(2025, 7, 9, 18, 11, 31, 114597)


def test_class_user_response(user_response):
    assert isinstance(user_response, UserResponse)


def test_user_response_optinal_fields():
    user = UserResponse(
        id=15, name='Test User', email='testuser@email.com', 
        created_at=datetime(2025, 7, 9, 18, 11, 31, 114597), 
    )
    assert user.updated_at is None
    assert user.deleted_at is None


def test_user_response_invalid_data():
    with pytest.raises(ValidationError):
        user = UserResponse()


def test_schema_user_update_success(user_update):
    assert user_update.new_name == 'Test User'
    assert user_update.new_email == 'testuser@email.com'
    assert user_update.new_password == 'mynewpassword'


def test_schema_user_update_optional_fields():
    user=UserUpdate()
    assert user.new_name is None
    assert user.new_email is None
    assert user.new_password is None


def test_class_user_update(user_update):
    assert isinstance(user_update, UserUpdate)


def test_user_response_is_datetime(user_response):
    assert isinstance(user_response.created_at, datetime)
    assert isinstance(user_response.deleted_at, datetime)