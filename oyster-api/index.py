from fastapi import FastAPI, Query
from typing import List
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import api.homeController as homeController
import api.dataController as dataController
import flairNLP.preprocessingController as preproController


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

class Model(BaseModel):
    name: str
    type: str
    rawDatasetId: str
    processedDatasetId: str

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

@app.delete("/dataset/{datasetID}")
async def  deleteDatasets(datasetID: str):
    if(datasetID == "all"):
        return await dataController.resetDataSets()
    return
    

@app.get("/dataset/{datasetID}")
async def datasetRows(datasetID: str):
    return await dataController.getDatasetRows(datasetID)

@app.get("/dataset/{datasetID}/{index}")
async def datasetRows(datasetID: str, index: int):
    return await dataController.getDatasetRowsBatch(datasetID, index)

@app.post("/dataset/{datasetID}")
async def datasetRow(datasetID: str, datasetRow: DatasetRow):
    return await dataController.createDatasetRow(datasetID, datasetRow.dict())

@app.get("/model")
async def getModels():
    return await dataController.getAllModels()

@app.post("/model") 
async def createModel(model: Model):
    name = model.dict().get("name")
    type = model.dict().get("type")
    rawDatasetId = model.dict().get("rawDatasetId")
    return await dataController.createModel(name, type, rawDatasetId)

@app.get("/preprocessing")
async def preprocessing():
    return await preproController.getPreprocessingEnums()

@app.get("/preprocessing/apply/{datasetID}")
async def applyPreprocessing(datasetID: str, preprocessing: List[str] = Query(None)):
    return await preproController.applyPreprocessing(preprocessing, datasetID)   

@app.get("/trainmodel")
async def trainModel():
    return await flairController.train()

@app.get("/predict/")
async def trainModel(text: str):
    return await flairController.predict(text)
