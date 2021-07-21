from fastapi import FastAPI
import api.homeController as homeController
import api.dataController as dataController
from pydantic import BaseModel

VERSION = 'v0.0.1'

# App
# --------------------

app = FastAPI()


# Model
# --------------------

class DatasetRow(BaseModel):
    data: str

# Routes
# --------------------

@app.get("/")
async def root():
    return {"Oyster API": VERSION}

@app.get("/home")
async def home():
    return await homeController.helloHome()

@app.get("/dataset")
async def data():
    return await dataController.getAll()

@app.post("/dataset")
async def data(row: DatasetRow):
    print(row)
    return await dataController.insert(row.dict())