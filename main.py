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

app = FastAPI()
# app.mount("/static", StaticFiles(directory = "public"))

@app.get("/")
def root():
    return {"message": "Hello World"}

# @app.get("/")
# async def hello():
#    return {"message": "Hello world"}


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

        
    with open(file.filename, 'r') as f:
        # Работа второй модели
        res_preds = find_secrets(file.filename)

    os.remove(file.filename)
    return res_preds 

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload = True)




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





