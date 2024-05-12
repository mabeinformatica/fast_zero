from datetime import datetime
from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'name': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
            'role': 1,
            'avatar': 'http://example.com',
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'name': 'alice',
        'email': 'alice@example.com',
        'role': 1,
        'avatar': 'http://example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'bob',
            'email': 'teste@test.com',
            'password': 'mynewpassword',
            'role': 2,
            'avatar': 'http://example.com',
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'name': 'bob',
        'email': 'teste@test.com',
        'role': 2,
        'avatar': 'http://example.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
            'role': 2,
            'avatar': 'http://example.com',
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert response.json() == {'detail': 'Not enough permissions'}