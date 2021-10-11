import api.repo as repo
from api.repo import TableName
import api.modelDataController as modelData
import uuid

# Dataset
# ----------

async def createDataset(name):
    dataset = {
        "id": str(uuid.uuid4()),
        "name": name
    }
    await repo.insert(TableName.DATASET, dataset)
    return dataset

async def getAllDataset():
    return await repo.getAll(TableName.DATASET)

async def resetDataSets():
    return await repo.resetDatabase()


# Dataset Rows
# ----------

async def getDatasetRows(id):
    return await repo.getFilteredDocuments(TableName.DATESET_ITEMS, fieldKey='dataset_id', fieldValue=id)

async def createDatasetRow(id, row):

    row['id'] = str(uuid.uuid4())
    row['dataset_id'] = id
    return await repo.insert(TableName.DATESET_ITEMS, row)

# Returns row of dataset at index
async def getDatasetRowsBatch(id, index):
    results = await repo.getFilteredDocuments(TableName.DATESET_ITEMS, fieldKey='dataset_id',fieldValue=id)
    return results[index]


# ENTITY_TAG_SET
# --------------

async def getAllEntityTagSets():
    return await repo.getAll(TableName.ENTITY_TAG_SET)

async def insertEntityTagSet(name: str, rawDatasetId: str, processes: list):
    entityTagSet = {
        "id": str(uuid.uuid4()),
        "name": name,
        "rawDatasetId": rawDatasetId,
        "processes" : processes
    }
    await repo.insert(TableName.ENTITY_TAG_SET, entityTagSet)
    return entityTagSet

# ENTITY_TAG_SET_ITEM
# ---------------

async def getEntityTagSetItems(entityTagSetId) :
    results = await repo.getFilteredDocuments(TableName.ENTITY_TAG_SET, 'id', entityTagSetId)
    return results[0]

async def getEntityTagSetItemsValue(entityTagSetId) :
    results = await repo.getFilteredDocuments(TableName.ENTITY_TAG_SET_ITEMS, 'id', entityTagSetId)
    return results[0]

async def insertEntityTagSetItem(entityTagSetId: str, rawTextRowId: str, tags :  list):
    entityTagSetItem = {
        "id": str(uuid.uuid4()),
        "entityTagSetId": entityTagSetId,
        "rawTextRowId" : rawTextRowId,
        "tags" : tags
    }
    await repo.insert(TableName.ENTITY_TAG_SET_ITEMS, entityTagSetItem)
    return entityTagSetItem

async def saveNERTags(modelId:str, rowId: str, tags: list):
    model = await modelData.getModel(modelId=modelId)
    processedDatasetId = model["processedDatasetId"]
    entityTagSet = await getEntityTagSetItems(processedDatasetId)
    rawDatasetId = entityTagSet["rawDatasetId"]
    return await insertEntityTagSetItem(entityTagSet["id"], 
                            rawTextRowId=rowId,
                            tags=tags)