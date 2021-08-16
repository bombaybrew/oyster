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

    # Create empty  dataset to save tags related to raw dataset. 
    # Replace "processes" hardcoded values with user input.
    entityTagSet = await insertEntityTagSet(name,rawDatasetId,processes=["STOPWORD", "PUNCTUATION", "LAMMATIZE", "JUNK"])
    model["processedDatasetId"] = entityTagSet["id"]
    await repo.insert(repo.TABLE_MODEL, model)
    return model

async def getAllModels():
    return await repo.getAll(repo.TABLE_MODEL)

# Model versions
# ----------

async def getModel(modelId):
    return await repo.getModelItems(modelId)

async def createModelRow(modelId, modelVersion, row):
    return await repo.insertModelItems(modelId, modelVersion,row)

# ENTITY_TAG_SET
# --------------

async def getAllEntityTagSets():
    return await repo.getAllEntityTagSets()

async def insertEntityTagSet(name: str, rawDatasetId: str, processes: list):
    entityTagSet = {
        "id": str(uuid.uuid4()),
        "name": name,
        "rawDatasetId": rawDatasetId,
        "processes" : processes
    }
    await repo.insertEntityTagSet(entityTagSet)
    return entityTagSet

# ENTITY_TAG_SET_ITEM
# ---------------

async def getEntityTagSetItems(entityTagSetId) :
    return await repo.getEntityTagItems(entityTagSetId)

async def insertEntityTagSetItem(entityTagSetId: str, rawTextRowId: str, tags :  list):
    entityTagSetItem = {
        "id": str(uuid.uuid4()),
        "entityTagSetId": entityTagSetId,
        "rawTextRowId" : rawTextRowId,
        "tags" : tags
    }
    await repo.insertEntityTagSetItem(entityTagSetItem)
    return entityTagSetItem

async def saveNERTags(modelId:str, rowId: str, tags: list):
    model = await getModel(modelId=modelId)
    processedDatasetId = model["processedDatasetId"]
    entityTagSet = await repo.getEntityTagSet(processedDatasetId)
    rawDatasetId = entityTagSet["rawDatasetId"]
    return await insertEntityTagSetItem(entityTagSet["id"], 
                            rawTextRowId=rowId,
                            tags=tags)
