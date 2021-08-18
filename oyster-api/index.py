from fastapi import FastAPI, Query
from typing import List
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import api.homeController as homeController
import api.dataController as dataController
import nlp.preprocessingController as preproController
import nlp.nlpController as nlpController


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
    support: str
    rawDatasetId: str
    processedDatasetId: str

class EntityTagSet(BaseModel):
    name: str
    rawDataset: str
    processes: list

class EntityTagSetRow(BaseModel):
    entityTagSetId: str
    rawTextRowId: str
    tags : list

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

@app.get("/preprocessing")
async def preprocessing():
    return await preproController.getPreprocessingEnums()

@app.get("/preprocessing/apply/{datasetID}")
async def applyPreprocessing(datasetID: str, preprocessing: List[str] = Query(None)):
    return await preproController.applyPreprocessing(preprocessing, datasetID)


@app.get("/test/model/{modelID}")
async def testModel(modelID:str, text: str):
    return await nlpController.testModel(modelID, text)

@app.post("/experiment/model") 
async def createModel(model: Model):
    name = model.dict().get("name")
    type = model.dict().get("type")
    support = model.dict().get("support")
    rawDatasetId = model.dict().get("rawDatasetId")
    modelId = await dataController.createModel(name, type, support, rawDatasetId)
    return modelId

@app.get("/experiment/model")
async def getModels():
    return await dataController.getAllModels()

@app.get("/experiment/model/{modelID}")
async def getModels(modelID:str):
    return await dataController.getModel(modelID)

@app.post("/experiment/model/{modelId}/tags/{rawTextRowId}")
async def saveTags(modelId: str, rawTextRowId: str, tags: list):
    return await dataController.saveNERTags(modelId,rowId=rawTextRowId, tags= tags)

@app.get("/experiment/entitytagsets")
async def getAllEntityTagSets():
    return await dataController.getAllEntityTagSets()

@app.get("/experiment/entitytagsets/{entityTagSetId}")
async def getAllEntityTagSets(entityTagSetId: str):
    return await dataController.getEntityTagSetItems(entityTagSetId)
