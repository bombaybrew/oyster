from os import wait
from flair import data
import api.repo as repo
import uuid
import  pandas as pd

# Dataset
# ----------

async def createDataset(name):
    dataset = {
        "id": str(uuid.uuid4()),
        "name": name
    }
    await repo.insert(repo.TABLE_DATASET, dataset)
    return dataset

async def getAllDataset():
    return await repo.getAll(repo.TABLE_DATASET)


# Dataset Rows
# ----------

async def getDatasetRows(id):
    return await repo.getAllDatasetItems(id)

async def createDatasetRow(id, row):

    row['id'] = str(uuid.uuid4())
    return await repo.insertDatasetItems(id, row)

# Returns row of dataset at index
async def getDatasetRowsBatch(id, index):
    return await repo.getDatasetItems(id, index)

# Clears all table 
async def resetDataSets():
    # await repo.clearDatasetItemsTable()
    # await repo.clearDatasetTable()
    await repo.resetDaset()
    return "Success"


# Model
# ----------

async def createModel(name, type, rawDatasetId):
    model = {
        "id": str(uuid.uuid4()),
        "name": name,
        "type":type,
        "rawDatasetId": rawDatasetId,
        "progress": 0
    }
    dataset = {
        "id": str(uuid.uuid4()),
        "name": "Processed for " + name + " model",
        "rawDatasetId": rawDatasetId,
        "version" : 0
    }
    await repo.insert(repo.TABLE_DATASET, dataset)
    model["processedDatasetId"] = dataset["id"]
    await repo.insert(repo.TABLE_MODEL, model)
    return model

async def getAllModels():
    return await repo.getAll(repo.TABLE_MODEL)

# Model versions
# ----------

async def getModelRows(modelId):
    return await repo.getModelItems(modelId)

async def createModelRow(modelId, modelVersion, row):
    return await repo.insertModelItems(modelId, modelVersion,row)