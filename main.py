import os
import time
import shutil
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import uvicorn

from project_program import model1, model2
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

        
    with open(file.filename, 'r') as f:
        # Работа первой модели
        passwords_mas = model1(file.filename)
        # Работа второй модели
        res_preds = model2(file.filename)
        #Файл json с результатом
        snippets_with_pass = res_preds[res_preds['Target'] == 1]['Snippet'].tolist()

    os.remove(file.filename)
    return {"snippets": snippets_with_pass}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload = True)




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





