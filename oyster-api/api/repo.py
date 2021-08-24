from os import remove
from tinydb import TinyDB, Query, table, where
from tinydb.utils import D
import enum

db = TinyDB('data/tinydb.json')
class TableName(enum.Enum):
    # Used for saving Named Entities of particular row in raw dataset
    ENTITY_TAG_SET = "ner_tags_set"
    ENTITY_TAG_SET_ITEMS = "ner_tags_items"

    DATASET = "dataset"
    DATESET_ITEMS = "dataset_items"
    MODEL = "model"
    MODEL_ITEMS = "model_items"


async def insert(tableName, row):
    table = db.table(tableName.value)
    return table.insert(row)

async def getAll(tableName):
    table = db.table(tableName.value)
    return table.all()

async def getTable(tableName):
    return db.table(tableName.value)

async def getFilteredDocuments(tableName, fieldKey, fieldValue):
    table = db.table(tableName.value)
    return table.search(where(fieldKey) == fieldValue)

async def resetDatabase():
    for table in TableName:
        db.drop_table(table.value)
    return
