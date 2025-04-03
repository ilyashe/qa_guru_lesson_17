import requests
from jsonschema import validate
import schemas

url = 'https://reqres.in'

users_endpoint = '/api/users/'
register_endpoint = '/api/register'


def test_get_single_user():
    user_id = '2'
    response = requests.get(url + users_endpoint + user_id)

    assert response.status_code == 200
    validate(response.json(), schema=schemas.get_single_user)

def test_get_single_user_not_found():
    user_id = '23'
    response = requests.get(url + users_endpoint + user_id)

    assert response.status_code == 404

def test_create_user():
    name = 'ivan'
    job = 'lawyer'

    payload = {
        'name': name,
        'job': job
    }

    response = requests.post(url + users_endpoint, json=payload)

    assert response.status_code == 201
    validate(response.json(), schema=schemas.create_user)

def test_update_user():
    name = 'ivan'
    job = 'lawyer'
    user_id = '2'

    payload = {
        'name': name,
        'job': job
    }

    response = requests.put(url + users_endpoint + user_id, json=payload)

    assert response.status_code == 200
    validate(response.json(), schema=schemas.update_user)

def test_delete_user():
    user_id = '2'

    response = requests.delete(url + users_endpoint + user_id)

    assert response.status_code == 204

def test_register_user():
    email = 'eve.holt@reqres.in'
    password = 'pistol'

    payload = {
    'email': email,
    'password': password
    }

    response = requests.post(url + register_endpoint, json=payload)

    assert response.status_code == 200
    validate(response.json(), schema=schemas.register_successful)

def test_register_user_without_password():
    email = 'eve.holt@reqres.in'

    payload = {
    'email': email
    }

    response = requests.post(url + register_endpoint, json=payload)

    assert response.status_code == 400
    validate(response.json(), schema=schemas.register_unsuccessful)

def test_should_user_in_users_list():
    user_id = 8
    email = 'lindsay.ferguson@reqres.in'
    last_name = 'Ferguson'

    response = requests.get(url + users_endpoint, params={'page': '2'})
    print(response.json())

    assert response.status_code == 200
    users_id = {user['id']: (user['email'], user['last_name']) for user in response.json()['data']}
    assert user_id in users_id
    assert users_id[user_id] == (email, last_name)
