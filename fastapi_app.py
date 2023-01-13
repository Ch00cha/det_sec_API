import os
import time
import shutil
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import uvicorn

# from project_program import find_secrets
# from путь к нашей программе

class Item(BaseModel):
    text: str

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

        
    with open(file.filename, 'r') as f:
        # Работа второй модели
        res_preds = len(file.filename)
    f_name = file.filename
    os.remove(file.filename)
    return {f_name : res_preds} 


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





