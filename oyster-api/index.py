from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import api.homeController as homeController
import api.dataController as dataController


VERSION = 'v0.0.1'

# App
# --------------------

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Model
# --------------------

class Dataset(BaseModel):
    name: str

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
async def dataset():
    return await dataController.getAllDataset()

@app.post("/dataset")
async def dataset(dataset: Dataset):
    return await dataController.createDataset(dataset.dict().get("name"))

@app.get("/dataset/{datasetID}")
async def datasetRows(datasetID: str):
    return await dataController.getDatasetRows(datasetID)

@app.post("/dataset/{datasetID}")
async def datasetRow(datasetID: str, datasetRow: DatasetRow):
    return await dataController.createDatasetRow(datasetID, datasetRow.dict())