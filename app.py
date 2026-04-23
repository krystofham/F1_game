from fastapi import FastAPI
import json

app = FastAPI()

data = 
@app.get("/")
def index():
    return {"Hello": "World"}