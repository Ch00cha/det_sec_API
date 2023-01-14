from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from project_program import find_secrets

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world"}
#   assert "status" in result


def test_model():
    prediction = find_secrets('https://api.github.com/repos/Ch00cha/det_sec_API/contents/snipet_with_pass.txt')
    assert prediction == {3: 'String password = ""Stargate1"";'}


# def test_with_pass():
#     response = client.post('/predict',
#         input = файл
#     )
#   res = response.input()
#   assert response.status_code == 200
#   assert res == ?

# def test_without_pass():
  
