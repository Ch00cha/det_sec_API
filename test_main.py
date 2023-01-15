from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_app import app
from fastapi_app import find_secrets

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}


def test_model_with_pass():
    prediction = find_secrets('snipet_with_pass.txt')
    assert prediction == {3: 'String password = ""Stargate1"";'}
    
    
def test_model_with_pass():
    prediction = find_secrets('snip_without_pass.txt')
    assert prediction == 'Пароли не найдены'

    
def test_with_pass():
    response = client.post('/uploadfile', input = 'snipet_with_pass.txt')
    assert response.status_code == 200
    assert response == {3: 'String password = ""Stargate1"";'}


def test_repo():
    response = client.post('/predict', url = 'https://github.com/Ch00cha/det_sec_API')
    assert response.status_code == 200
    assert response == {'README.md': 'Пароли не найдены', 'api_requests.py': 'Пароли не найдены', 'fastapi_app.py': 'Пароли не найдены', 'model_app.py': 'Пароли не найдены', 'requirements.txt': 'Пароли не найдены', 'test_file.txt': {'3': 'String password = ""Stargate1"";'}, 'test_main.py': 'Пароли не найдены', 'web_app.py': 'Пароли не найдены'}


# def test_without_pass():
  
