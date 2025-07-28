import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def create_user(client, db_session):
    user = {'name': 'Alice', 'email': 'alice@example', 'password': '123456'}
    response = client.post('/user/new/', json=user)
    return response


@pytest.fixture
def content_data():
    return {'user_id': 1, 'title': 'Test', 'content': 'test content'}


@pytest.fixture
def create_content(client, db_session, content_data):
    response = client.post('/content/create/', json=content_data)
    return response


@pytest.fixture
def keys_content_response():
    return ['id', 'user_id', 'title', 'content', 'created_at',
            'updated_at', 'deleted_at'
            ]


def test_create_content_with_valid_data(
        client, db_session, create_user, create_content, keys_content_response
        ):
    create_user
    response = create_content
    assert response.status_code == 200

    data = response.json()
    for key in keys_content_response:
        assert key in data
    assert data['id'] == 1
    assert data['user_id'] == 1
    assert data['title'] == 'Test'
    assert data['content'] == 'test content'
    assert data['created_at'] is not None
    assert data['updated_at'] is None
    assert data['deleted_at'] is None


def test_create_user_with_empty_fields(client, create_user):
    create_user
    response = client.post('/content/create/', json={})
    assert response.status_code == 422


def test_get_users_success(
        client, db_session, create_user, create_content, keys_content_response
        ):
    create_user
    create_content
    response = client.get('/content/list/')
    assert response.status_code == 200

    data = response.json()
    for key in keys_content_response:
        assert key in data[0]
    assert data[0]['id'] == 1
    assert data[0]['user_id'] == 1
    assert data[0]['title'] == 'Test'
    assert data[0]['content'] == 'test content'
    assert data[0]['created_at'] is not None
    assert data[0]['updated_at'] is None
    assert data[0]['deleted_at'] is None


def test_update_content_success(
        client, db_session, create_user, create_content, keys_content_response
        ):
    create_user
    create_content
    update = {'user_id': 1, 'new_title': 'new', 'new_content': 'new new'}
    response = client.put('/content/update/1/', json=update)
    assert response.status_code == 200

    data = response.json()
    for key in keys_content_response:
        assert key in data
    assert data['id'] == 1
    assert data['user_id'] == 1
    assert data['title'] == 'new'
    assert data['content'] == 'new new'
    assert data['created_at'] is not None
    assert data['updated_at'] is not None
    assert data['deleted_at'] is None


def test_delete_user_success(client, create_user, create_content):
    create_user
    create_content
    response = client.delete('/content/delete/1')
    assert response.status_code == 200
    data = response.json()
    assert data['deleted_at'] is not None


def test_delete_user_with_invalid_content(client, db_session):
    response = client.delete('/content/delete/99999')
    assert response.status_code == 404