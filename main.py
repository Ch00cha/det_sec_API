import os

import shutil
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import requests
# from путь к нашей программе

app = FastAPI()
# app.mount("/static", StaticFiles(directory = "public"))




@app.get("/")
async def hello():
    return {"message": "Hello world"}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # content = file.file.read()  
        with open(file.filename, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message":"ERROR uploading file"}
    finally:
        file.file.close()
    with open(file.filename, "r") as f:
        for line in f:
            a = str(line)
            break
        f.close()
    os.remove(file.filename)
    return {"text": a}




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





