import api.repo as repo
import uuid

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
    return await repo.getDatasetItems(id)

async def createDatasetRow(id, row):
    return await repo.insertDatasetItems(id, row)
