!pip httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
client = TestClient(app)

@app.get("/")
def root():
    return {"message": "Hello World"}
  
def test_read_main():
  response = client.get('/')
  assert response.status_code == 200
  assert response.json() == {"message": "Hello World"}

# def test_with_pass():
#   response = client.post(''),
#       file=''
#   )
#   file_data = 

#   assert = assert response.status_code == 200
#   assert file_data == ''

# def test_without_pass():
  