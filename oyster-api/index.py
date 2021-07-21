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