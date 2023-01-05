from fastapi import FastAPI
# from путь к нашей программе

app = FastAPI()
# здесь достается наша прога


# get-запрос на файл, который должен проверятья
@app.get("/")
async def root():
    return {"message": "Hello"}

# post-запрос с выводом программы
@app.post("/predict/")
def predict():
    return {"message": "Hello"}    
