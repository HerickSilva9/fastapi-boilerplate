from datetime import datetime as dt

from pydantic import ValidationError
import pytest

from app.schemas.content import ContentCreate, ContentResponse, ContentUpdate

@pytest.fixture
def content_create():
    return ContentCreate(user_id=5, title='Test', content='Test Content')


@pytest.fixture
def content_response():
    return ContentResponse(
        id=10, user_id=5, title='Test', content='Test Content', 
        created_at=dt(2025, 7, 9, 18, 11, 31, 114597), 
        updated_at=dt(2025, 7, 9, 18, 11, 31, 114597), 
        deleted_at=dt(2025, 7, 9, 18, 11, 31, 114597)
        )


@pytest.fixture
def content_update():
    return ContentUpdate(
        user_id=7, new_title='New Test', new_content='New Test Content'
        )


def test_schema_content_create_success(content_create):
    assert content_create.user_id == 5
    assert content_create.title == 'Test'
    assert content_create.content == 'Test Content'


def test_content_create_invalid_data():
    with pytest.raises(ValidationError):
        user = ContentCreate()


def test_schema_content_response_success(content_response):
    assert content_response.id == 10
    assert content_response.title == 'Test'
    assert content_response.content == 'Test Content'
    assert content_response.updated_at == dt(2025, 7, 9, 18, 11, 31, 114597)
    assert content_response.deleted_at == dt(2025, 7, 9, 18, 11, 31, 114597)


def test_class_contents(content_create, content_update, content_response):
    assert isinstance(content_create, ContentCreate)
    assert isinstance(content_update, ContentUpdate)
    assert isinstance(content_response, ContentResponse)
    assert isinstance(content_response.created_at, dt)
    assert isinstance(content_response.deleted_at, dt)


def test_content_response_optinal_fields():
    user = ContentResponse(
        id=10, user_id=5, content='Test Content', 
        created_at=dt(2025, 7, 9, 18, 11, 31, 114597), 
        )
    assert user.updated_at is None
    assert user.deleted_at is None


def test_content_response_invalid_data():
    with pytest.raises(ValidationError):
        user = ContentResponse()


def test_schema_content_update_success(content_update):
    assert content_update.user_id == 7
    assert content_update.new_title == 'New Test'
    assert content_update.new_content == 'New Test Content'


def test_schema_content_update_optional_fields():
    content=ContentUpdate(user_id=9)
    assert content.user_id == 9
    assert content.new_title is None
    assert content.new_content is None