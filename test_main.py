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

def test_scan_rep():
    result = github_scan_rep('https://github.com/Ch00cha/det_sec_API/blob/main/test_file.txt')
    assert result == [   {   'content': 'Ii8vV2lGaQpTdHJpbmcgc3NpZCA9ICIiRlJJVFohQm94IDY1OTEgQ2FibGUg\n'
                   'Q1ciIjsKU3RyaW5nIHBhc3N3b3JkID0gIiJTdGFyZ2F0ZTEiIjsKLy9BdXRv\n'
                   'IHJlYm9vdCB3aGVuIG5vdCBjb25uZWN0ZWQgdG8gV2lGaQpsb25nIGRlbGF5\n'
                   'UmVib290ID0gMTAgKiAxMDAwOyAvL21zCi8vVm9sdW1pbwpTdHJpbmcgaG9z\n'
                   'dCA9ICIiIiI7CmludCBwb3J0ID0gODA7IiwxCiIjZGVmaW5lIEJTUF9VU0lO\n'
                   'R19BSFQxMAojZGVmaW5lIEJTUF9VU0lOR19URl9DQVJECiNkZWZpbmUgQlNQ\n'
                   'X1VTSU5HX0ZMQVNICiNkZWZpbmUgU1BJX0ZMQVNIX0RFVklDRV9OQU1FICIi\n'
                   'bm9yZmxhc2giIgojZGVmaW5lIFNQSV9GTEFTSF9UWVBFX05BTUUgIiJ3MjVx\n'
                   'MTI4IiIKI2RlZmluZSBCU1BfVVNJTkdfQVAzMjE2QyIsMAoiY29uc3QgY2hh\n'
                   'ciBjb25zb2xlQ2xhc3M6OnNldE1ldHJpY0ltcENtZFtdIFBST0dNRU0gPSAi\n'
                   'Im1ldGltcCIiOwpjb25zdCBjaGFyIGNvbnNvbGVDbGFzczo6c2V0TWV0cmlj\n'
                   'SW1wRGVzY1tdIFBST0dNRU0gPSAiIlswfDFdIDAgPSBNZXRyaWMgMSA9IElt\n'
                   'cGVyaWFsIiI7Ig==\n',
        'name': 'test_file.txt'}]
    
# def test_with_pass():
#     response = client.post('/uploadfile', input = 'test_file.txt')
#     assert response.status_code == 200
#     assert response == {3: 'String password = ""Stargate1"";'}


# def test_repo():
#     content = request_to_det_sec_API('https://github.com/Ch00cha/det_sec_API')
#     response = client.post('/predict', json=content)
#     assert response.status_code == 200
#     assert response == {'README.md': 'Пароли не найдены', 'api_requests.py': 'Пароли не найдены', 'fastapi_app.py': 'Пароли не найдены', 'model_app.py': 'Пароли не найдены', 'requirements.txt': 'Пароли не найдены', 'test_file.txt': {'3': 'String password = ""Stargate1"";'}, 'test_main.py': 'Пароли не найдены', 'web_app.py': 'Пароли не найдены'}

  
