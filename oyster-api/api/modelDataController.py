from os import wait
from flair import data
import api.repo as repo
from api.repo import TableName
import uuid
import  pandas as pd
import api.dataSetController as dataSetController 

# Clears all table 
async def resetDataBase():
    await repo.resetDatabase()
    return "Success"


# Model
# ----------

async def createModel(name, type, support, rawDatasetId, nerTags):
    model = {
        "id": str(uuid.uuid4()),
        "name": name,
        "type":type,
        "support": support,
        "rawDatasetId": rawDatasetId,
        "progress": 0,
        "ner_tags" : nerTags
    }

    # Create empty  dataset to save tags related to raw dataset. 
    # Replace "processes" hardcoded values with user input.
    entityTagSet = await dataSetController.insertEntityTagSet(name,rawDatasetId,processes=["STOPWORD", "PUNCTUATION", "LAMMATIZE", "JUNK"])
    model["processedDatasetId"] = entityTagSet["id"]
    await repo.insert(TableName.MODEL, model)
    return model

async def getAllModels():
    return await repo.getAll(TableName.MODEL)

# Model versions
# ----------

async def getModel(modelId):
    results = await repo.getFilteredDocuments(TableName.MODEL, 'id',  modelId)
    return results[0]

async def createModelRow(modelId, modelVersion, row):
    row["model_id"] = id
    row["model_version"] = modelVersion
    return await repo.insert(TableName.MODEL_ITEMS, row)
    # return await repo.insertModelItems(modelId, modelVersion,row)

