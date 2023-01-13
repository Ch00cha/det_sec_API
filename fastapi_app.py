import os
import time
import shutil
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import uvicorn

from project_program import find_secrets
# from путь к нашей программе

class Item(BaseModel):
    text: str

app = FastAPI()
# app.mount("/static", StaticFiles(directory = "public"))


@app.get("/")
async def hello():
    return {"message": "Hello world"}


@app.post("/predict")
async def predict(item: Item):
    prediction = find_secrets(item.text)
    return prediction


if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", reload = True)




# @app.post("/uploadfile")
# async def create_upload_file(file: UploadFile = File(...)):
#     try:
#         with open(file.filename, "r") as f:
#             for line in f:
#                 a = str(line)
#     except Exception:
#         return {"message":"ERROR1"}
#     finally:
#         file.file.close()    
#     return {"text": a}





