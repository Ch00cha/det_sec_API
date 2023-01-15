# from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_app import app, find_secrets
from api_requests import request_to_det_sec_API

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}


def test_model_with_pass():
    prediction = find_secrets('test_file.txt')
    assert prediction == {3: 'String password = ""Stargate1"";'}
    
    
def test_model_without_pass():
    prediction = find_secrets('snip_without_pass.txt')
    assert prediction == 'Пароли не найдены'

    
# def test_with_pass():
#     response = client.post('/uploadfile', input = 'test_file.txt')
#     assert response.status_code == 200
#     assert response == {3: 'String password = ""Stargate1"";'}


def test_repo():
    content = request_to_det_sec_API('https://github.com/Ch00cha/det_sec_API')
    response = client.post('/predict', json=content)
    assert response.status_code == 200
    assert response == {'README.md': 'Пароли не найдены', 'api_requests.py': 'Пароли не найдены', 'fastapi_app.py': 'Пароли не найдены', 'model_app.py': 'Пароли не найдены', 'requirements.txt': 'Пароли не найдены', 'test_file.txt': {'3': 'String password = ""Stargate1"";'}, 'test_main.py': 'Пароли не найдены', 'web_app.py': 'Пароли не найдены'}

  
