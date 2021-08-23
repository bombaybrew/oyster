from os import remove
from tinydb import TinyDB, Query, table, where
from tinydb.utils import D

db = TinyDB('data/tinydb.json')

TABLE_DATASET = "dataset"
TABLE_DATESET_ITEMS = "dataset_items"
TABLE_MODEL = "model"
# TABLE_MODEL_ITEMS :  model versions
TABLE_MODEL_ITEMS = "model_items"

# Used for saving Named Entities of particular row in raw dataset
TABLE_ENTITY_TAG_SET = "ner_tags_set"
TABLE_ENTITY_TAG_SET_ITEMS = "ner_tags_items"

async def insert(tableName, row):
    table = db.table(tableName)
    return table.insert(row)

async def getAll(tableName):
    table = db.table(tableName)
    return table.all()

async def getTable(tableName):
    return db.table(tableName)

async def getAllDatasetItems(datasetId):
    print(datasetId)
    table = db.table(TABLE_DATESET_ITEMS)
    return table.search(where('dataset_id') == datasetId)
    # return db.table(TABLE_DATESET_ITEMS).all()

async def getDatasetItems(datasetId, index):
    table = db.table(TABLE_DATESET_ITEMS)
    return table.search(where('dataset_id') == datasetId)[index]

async def insertDatasetItems(datasetID, row):
    row['dataset_id'] = datasetID

    table = db.table(TABLE_DATESET_ITEMS)
    return table.insert(row)

# Drop TABLE_DATESET_ITEMS
# async def clearDatasetItemsTable():
#     return db.drop_table(TABLE_DATESET_ITEMS)

async def resetDaset():
    db.drop_table(TABLE_DATASET)
    db.drop_table(TABLE_DATESET_ITEMS)
    db.drop_table(TABLE_MODEL)
    return

# MODEL_ITEMS
# # -----------

async def getModelItems(id):

    table = db.table(TABLE_MODEL)
    return table.search(where('id') == id)[0]

async def insertModelItem(modelId, model_version, row):
    row["model_id"] = id
    row["model_version"] = model_version
    table = db.table(TABLE_MODEL_ITEMS)
    return table.insert(row)


# ENTITY_TAG_SET
# ---------------

async def getAllEntityTagSets():
    table = db.table(TABLE_ENTITY_TAG_SET)
    return table.all()

async def getEntityTagSet(id):
    table = db.table(TABLE_ENTITY_TAG_SET)
    print("getEntityTagSet id === ")
    print(id)
    return table.search(where("id") == id)[0]


async def insertEntityTagSet(row):
    table = db.table(TABLE_ENTITY_TAG_SET)
    return table.insert(row)

# ENTITY_TAG_SET_ITEMS
# ---------------

async def getEntityTagItems(entityTagSetId):
    table = db.table(TABLE_ENTITY_TAG_SET_ITEMS)
    return table.search(where('entityTagSetId') == entityTagSetId)


async def insertEntityTagSetItem(row):
    table = db.table(TABLE_ENTITY_TAG_SET_ITEMS)
    return table.insert(row)