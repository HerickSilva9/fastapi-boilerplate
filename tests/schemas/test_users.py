from datetime import datetime as dt

from pydantic import ValidationError
import pytest

from app.schemas.user import UserCreate, UserResponse, UserUpdate


@pytest.fixture
def user_create():
    return UserCreate(
        name='Test User', email='user@email', password='mypassword'
        )


@pytest.fixture
def user_response():
    return UserResponse(
        id=15, name='Test User', email='user@email', 
        created_at=dt(2025, 7, 9, 18, 11, 31, 114597), 
        updated_at=dt(2025, 7, 9, 18, 11, 31, 114597), 
        deleted_at=dt(2025, 7, 9, 18, 11, 31, 114597)
    )


@pytest.fixture
def user_update():
    return UserUpdate(
        new_name='newUser', new_email='user@email', new_password='newpassword'
        )


def test_schema_user_create_success(user_create):
    assert user_create.name == 'Test User'
    assert user_create.email == 'user@email'
    assert user_create.password == 'mypassword'


def test_user_create_invalid_data():
    with pytest.raises(ValidationError):
        user = UserCreate()


def test_schema_user_response_success(user_response):
    assert user_response.id == 15
    assert user_response.name == 'Test User'
    assert user_response.email == 'user@email'
    assert user_response.updated_at == dt(2025, 7, 9, 18, 11, 31, 114597)
    assert user_response.deleted_at == dt(2025, 7, 9, 18, 11, 31, 114597)


def test_user_response_optinal_fields():
    user = UserResponse(
        id=15, name='Test User', email='user@email', 
        created_at=dt(2025, 7, 9, 18, 11, 31, 114597), 
        )
    assert user.updated_at is None
    assert user.deleted_at is None


def test_user_response_invalid_data():
    with pytest.raises(ValidationError):
        user = UserResponse()


def test_schema_user_update_success(user_update):
    assert user_update.new_name == 'newUser'
    assert user_update.new_email == 'user@email'
    assert user_update.new_password == 'newpassword'


def test_schema_user_update_optional_fields():
    user=UserUpdate()
    assert user.new_name is None
    assert user.new_email is None
    assert user.new_password is None


def test_class_users(user_create, user_update, user_response):
    assert isinstance(user_create, UserCreate)
    assert isinstance(user_update, UserUpdate)
    assert isinstance(user_response, UserResponse)
    assert isinstance(user_response.created_at, dt)
    assert isinstance(user_response.deleted_at, dt)