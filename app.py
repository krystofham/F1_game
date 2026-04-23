from fastapi import FastAPI
from main import *

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}