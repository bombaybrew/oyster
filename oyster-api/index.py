from fastapi import FastAPI, Query
from fastapi.openapi.utils import get_openapi
from typing import List
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from functools import wraps
import math

import api.homeController as homeController
import api.dataController as dataController
import nlp.preprocessingController as preproController
import nlp.nlpController as nlpController
import constants.constants as constants


VERSION = 'v0.0.1'

# App
# --------------------

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8082",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API groupping tags
# -----------


def setOpenApi_shema():
    openapi_shema = get_openapi(
        title="Oyster API",
        version="v0.0.1",
        description="This is a very Oyster OpenAPI schema",
        routes=app.routes,
    )
    openapi_shema['tags'] = constants.api_tags_metadata
    app.openapi_schema = openapi_shema


# Decorators
# --------------------

def response_wrapper(func):
    @wraps(func)
    async def function_wrapper(*args, **kwargs):
        data = await func(*args, **kwargs)
        page = kwargs.get('page', 0)
        limit = kwargs.get('limit', 50)
        start = page * limit

        result = {}
        result["data"] = data[start: start + limit]
        result["error"] = {}
        total_rows = len(data)
        total_pages = math.ceil(total_rows/limit)
        pre = page - 1
        next = page + 1
        if page == 0:
            pre = -1
        if page == total_pages - 1:
            next = -1

        result["meta"] = {
            "count": len(data),
            "pages": total_pages,
            "pre_page": pre,
            "next_page": next
        }
        return result
    return function_wrapper

# Model
# --------------------


class Dataset(BaseModel):
    name: str


class DatasetRow(BaseModel):
    data: str


class NERTag(BaseModel):
    name: str
    range: str


class Model(BaseModel):
    name: str
    type: str
    support: str
    rawDatasetId: str
    processedDatasetId: str
    ner_tags: List[str]


class EntityTagSet(BaseModel):
    name: str
    rawDataset: str
    processes: list


class EntityTagSetRow(BaseModel):
    entityTagSetId: str
    rawTextRowId: str
    tags: List[NERTag]

# Routes
# --------------------


@app.get("/")
async def root():
    return {"Oyster API": VERSION}


@app.get("/home")
async def home():
    return await homeController.helloHome()


@app.get("/dataset",
         tags=[constants.METADATA_TAG_Dataset])
async def dataset():
    return await dataController.getAllDataset()


@app.post("/dataset", tags=[constants.METADATA_TAG_Dataset])
async def dataset(dataset: Dataset):
    return await dataController.createDataset(dataset.dict().get("name"))


@app.delete("/dataset/{datasetID}", tags=[constants.METADATA_TAG_Dataset])
async def deleteDatasets(datasetID: str):
    if(datasetID == "all"):
        return await dataController.resetDataSets()
    return


@app.get("/dataset/{datasetID}", tags=[constants.METADATA_TAG_Dataset])
@response_wrapper
async def datasetRows(datasetID: str, page: int = 0, limit: int = 50):
    result = await dataController.getDatasetRows(datasetID)
    return result


@app.get("/dataset/{datasetID}/{index}", tags=[constants.METADATA_TAG_Dataset])
async def datasetRows(datasetID: str, index: int):
    return await dataController.getDatasetRowsBatch(datasetID, index)


@app.post("/dataset/{datasetID}", tags=[constants.METADATA_TAG_Dataset])
async def datasetRow(datasetID: str, datasetRow: DatasetRow):
    return await dataController.createDatasetRow(datasetID, datasetRow.dict())


@app.get("/preprocessing", tags=[constants.METADATA_TAG_DataProcessing])
async def preprocessing():
    return await preproController.getPreprocessingEnums()


@app.get("/preprocessing/apply/{datasetID}", tags=[constants.METADATA_TAG_DataProcessing])
async def applyPreprocessing(datasetID: str, preprocessing: List[str] = Query(None)):
    return await preproController.applyPreprocessing(preprocessing, datasetID)


@app.get("/test/model/{modelID}", tags=[constants.METADATA_TAG_MLModel])
async def testModel(modelID: str, text: str):
    return await nlpController.testModel(modelID, text)


@app.get("/train/model/{modelID}/tags/{tagID}", tags=[constants.METADATA_TAG_MLModel])
async def trainModel(modelID: str, tagID: str):
    return await nlpController.trainModel(modelID, tagID)


@app.post("/experiment/model", tags=[constants.METADATA_TAG_Experiment])
async def createModel(model: Model):
    name = model.dict().get("name")
    type = model.dict().get("type")
    support = model.dict().get("support")
    rawDatasetId = model.dict().get("rawDatasetId")
    modelId = await dataController.createModel(name, type, support, rawDatasetId)
    await nlpController.createModel(modelId["id"])
    return modelId


@app.get("/experiment/model", tags=[constants.METADATA_TAG_Experiment])
async def getModels():
    return await dataController.getAllModels()


@app.get("/experiment/model/{modelID}", tags=[constants.METADATA_TAG_Experiment])
async def getModels(modelID: str):
    return await dataController.getModel(modelID)


@app.post("/experiment/model/{modelId}/tags/{rawTextRowId}", tags=[constants.METADATA_TAG_Experiment])
async def saveTags(modelId: str, rawTextRowId: str, tags: list):
    return await dataController.saveNERTags(modelId, rowId=rawTextRowId, tags=tags)


@app.get("/entitytagsets", tags=[constants.METADATA_TAG_ProcessedDataset])
async def getAllEntityTagSets():
    return await dataController.getAllEntityTagSets()


@app.get("/entitytagsets/{entityTagSetId}", tags=[constants.METADATA_TAG_ProcessedDataset])
async def getAllEntityTagSets(entityTagSetId: str):
    return await dataController.getEntityTagSetItems(entityTagSetId)

setOpenApi_shema()
