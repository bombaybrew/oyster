# code for uploading csv.

# async def insertCSVIntoDB(fileName): # fileName should be without extension
#     dataset = await createDataset(fileName)

#     dataFrame = pd.read_csv("data/" + fileName + ".csv")
#     for review in dataFrame.body:
#         await createDatasetRow(dataset["id"], {'data' : review})
#     return dataset