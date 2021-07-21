import api.repo as repo

async def insert(row):
    return await repo.insert(repo.TABLE_DATASET, row)

async def getAll():
    return await repo.getAll(repo.TABLE_DATASET)
