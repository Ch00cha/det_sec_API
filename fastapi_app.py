import os
import time
import shutil
import base64
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn

from project_program import find_secrets


def find_secrets_in_text(file_name, content):
    content = base64.b64decode(content).decode()
    file = open(str(file_name), 'w')
    file.write(content)
    file.close()
    predictions = find_secrets(str(file_name))
    os.remove(str(file_name))
    return predictions

class Item(BaseModel):
    path: list
    content: list

app = FastAPI()



@app.get("/")
async def hello():
    return {"message": "Hello world"}

@app.post("/predict")
async def predict(item: Item):
    result = {}
    read_json = Item.parse_raw(item)
    for i in range(len(read_json.path)):
        file_path = read_json.path[i]
        predictions = find_secrets_in_text(file_path, read_json.content[i])
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








