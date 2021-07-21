from tinydb import TinyDB, Query
db = TinyDB('data/tinydb.json')

TABLE_DATASET = "dataset"

async def insert(tableName, row):
    table = db.table(tableName)
    return table.insert(row)

async def getAll(tableName):
    table = db.table(tableName)
    return table.all()
