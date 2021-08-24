from nlp.preprocessing import PreprocessingEnum
import nlp.preprocessing as preprocessing
import api.dataSetController as dataSetControllder

async def getPreprocessingEnums():
    list = [process.name for process in PreprocessingEnum]
    return list

async def applyPreprocessing(preprocessingEnums, datasetId):
    list = await dataSetControllder.getDatasetRows(datasetId)
    text = [data['data'] for data in list]
    updatedText = preprocessing.startProcessing(preprocessingEnums, text)
    return updatedText

