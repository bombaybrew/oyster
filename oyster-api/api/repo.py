from tinydb import TinyDB, Query, where
db = TinyDB('data/tinydb.json')

TABLE_DATASET = "dataset"
TABLE_DATESET_ITEMS = "dataset_items"

async def insert(tableName, row):
    table = db.table(tableName)
    return table.insert(row)

async def getAll(tableName):
    table = db.table(tableName)
    return table.all()

async def getTable(tableName):
    return db.table(tableName)

async def getDatasetItems(datasetId):
    print(datasetId)
    table = db.table(TABLE_DATESET_ITEMS)
    return table.search(where('dataset_id') == datasetId)
    # return db.table(TABLE_DATESET_ITEMS).all()

async def insertDatasetItems(datasetID, row):

    row['dataset_id'] = datasetID

    table = db.table(TABLE_DATESET_ITEMS)
    return table.insert(row)
