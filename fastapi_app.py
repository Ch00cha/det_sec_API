import os
import shutil
import base64
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import uvicorn
from model_app import find_secrets


def find_secrets_in_text(content):
    content = base64.b64decode(content).decode()
    file = open("file.txt", 'w')
    file.write(content)
    file.close()
    try:
        predictions = find_secrets("file.txt")
    except:
        predictions = {"Error": "Ошибка сканирования файла"}
        os.remove("file.txt")
        return predictions
    else:
        os.remove("file.txt")
        return predictions


class Data(BaseModel):
    content: str
    name: str

class Item(BaseModel):
    accept: List[Data]

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Hello world"}

@app.post("/predict")
def predict(item: Item):
    result = {}
    read_json = Item.parse_obj(item)
    for i in range(len(read_json.accept)):
        file_path = read_json.accept[i].name
        predictions = find_secrets_in_text(read_json.accept[i].content)
        result.update({file_path : predictions})
    return result
    
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message":"ERROR uploading file"}
    finally:
        file.file.close()  
    res_preds = find_secrets(file.filename)
    f_name = file.filename
    os.remove(file.filename)
    return {f_name : res_preds} 


if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", reload = True)








