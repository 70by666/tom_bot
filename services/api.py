import requests

from settings import SUPERUSER_API_LOGIN, SUPERUSER_API_PASSWORD


def get_token():
    url = 'http://127.0.0.1:8000/auth/token/login/'
    response = requests.post(url=url, json={
        'username': SUPERUSER_API_LOGIN,
        'password': SUPERUSER_API_PASSWORD,
    })
    
    return response.json()['auth_token']


def get_user_from_id(user_id):
    url = f'http://127.0.0.1:8000/api/v1/user/{user_id}/' 
    response = requests.get(url=url, headers={
        'Authorization': f'Token {get_token()}',
    })
    result = response.json()
    if result['username'] == '':
        return False
    
    return result


def get_url_for_auth(user_id):
    url = f'http://127.0.0.1:8000/api/v1/geturl/{user_id}/'
    response = requests.get(url=url, headers={
        'Authorization': f'Token {get_token()}',
    })
    result = response.json()
    if result:
        return result
    else:
        return False
