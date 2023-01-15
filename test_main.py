from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_app import app
from fastapi_app import find_secrets

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}


def test_model():
    prediction = find_secrets('snipet_with_pass.txt')
    assert prediction == {3: 'String password = ""Stargate1"";'}


def test_with_pass():
    response = client.post('/uploadfile', input = 'snipet_with_pass.txt')
  assert response.status_code == 200
  assert response == {3: 'String password = ""Stargate1"";'}

# def test_without_pass():
  
