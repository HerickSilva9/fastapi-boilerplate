import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def user_data():
    return {"name": "Alice", "email": "alice@example", "password": "123456"}


@pytest.fixture
def create_user(client, db_session, user_data):
    response = client.post("/user/new/", json=user_data)
    return response


def test_create_user_with_valid_data(client, db_session, create_user):
    response = create_user

    assert response.status_code == 200
    
    data = response.json()
    assert ('id' and 'name' and 'email' and 'created_at') in data
    assert data['name'] == 'Alice'
    assert data['email'] == 'alice@example'
    assert data['updated_at'] is None
    assert data['deleted_at'] is None


def test_create_user_with_duplicated_email(client, db_session, user_data):
    first_user = client.post("/user/new/", json=user_data)
    second_user = client.post("/user/new/", json=user_data)
    assert first_user.status_code == 200
    assert second_user.status_code == 409


def test_create_user_with_empty_password(client, db_session, user_data):
    response = client.post("/user/new/", json={
        'name': 'Alice', 'email': 'alice@example', 'password': ''
        })
    assert response.status_code == 422


def test_create_user_with_empty_data(client):
    response_1 = client.post('/user/new/', json={})
    response_2 = client.post('/user/new/', json={
        'name': '', 'email': '', 'password': ''
        })

    assert response_1.status_code == 422
    assert response_2.status_code == 422

def test_get_users(client, db_session, create_user):
    create_user
    response = client.get('/user/list/')

    assert response.status_code == 200

    data = response.json()
    assert ('id' and 'name' and 'email' and 'created_at') in data[0]
    assert data[0]['name'] == 'Alice'
    assert data[0]['email'] == 'alice@example'
    assert data[0]['updated_at'] is None
    assert data[0]['deleted_at'] is None


def test_update_user_success(client, db_session, create_user):
    create_user
    update = {'new_name': 'Foo', 'new_email': '@email', 'new_password': '123'}
    response = client.put('/user/update/1/', json=update)
    
    assert response.status_code == 200
    
    data = response.json()
    assert ('id' and 'name' and 'email' and 'created_at') in data
    assert data['name'] == 'Foo'
    assert data['email'] == '@email'
    assert data['updated_at'] is not None
    assert data['deleted_at'] is None


def test_update_user_with_duplicated_email(client, db_session, create_user):
    create_user
    update = {'new_email': 'alice@example'}
    response = client.put('/user/update/1/', json=update)    
    assert response.status_code == 409


def test_delete_user_success(client, create_user):
    create_user
    response = client.delete('/user/delete/1')
    assert response.status_code == 200


def test_delete_user_with_invalid_user(client):
    response = client.delete('/user/delete/99999')
    assert response.status_code == 404