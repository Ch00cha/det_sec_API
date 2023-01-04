from fastapi import FastAPI
# from путь к нашей программе

app = FastAPI()
# здесь создается экземпляр класса нашей проги

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.post("/predict/")
def predict():
    return {"message": "Hello"}    
