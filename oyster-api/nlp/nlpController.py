# import nlp.prepareDataset as prepareDataset
import nlp.flairModel as flairModel
import api.dataController as dataController
import os.path
import os
import nlp.spacyModel as spacyModel
import enum

class ModelSupportEnum(enum.Enum):
    SPACY = 1
    FLAIR = 2

class ModelTpyeEnum(enum.Enum):
    NER = 1
    CLASSIFIER = 2
    
async def createModel(modelId):
    ## Get More info about model
    model = await dataController.getModel(modelId)
    modelType = model["type"].upper()
    modelSupport = model["support"].upper()
    if modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.SPACY.name:
        createSpacyNerModel(modelId)
    elif modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        createFlairNerModel(modelId)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.SPACY.name:
        return "Model type {modelType} or Model support {modelSupport} not  available"
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        return "Model type {modelType} or Model support {modelSupport} not  available"
    else:
        return "Model type {modelType} or Model support {modelSupport} not  available"
    return "Success"

def createSpacyNerModel(modelId):
    path = 'models/spacymodels/'+modelId+'/spacymodel'
    os.chmod('models',0o777) 
    os.makedirs(path)
    spacyModel.createModel(path)


def createFlairNerModel(modelId):
    path = 'models/flairmodels/'+modelId+'/flairmodel'
    os.chmod('models',0o777) 
    os.makedirs(path)
    flairModel.createModel(path)


## Test Models
async def testModel(modelId, text):
     ## Get More info about model
    model = await dataController.getModel(modelId)
    modelType = model["type"].upper()
    modelSupport = model["support"].upper()
    if modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.SPACY.name:
        return testSpacyNerModel(modelId, text)
    elif modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        return testFlairNerModel(modelId, text)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.SPACY.name:
        return testSpacyClassifierModel(modelId, text)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        return testFlairClassifierModel(modelId, text)
    else:
        return "Model type {modelType} or Model support {modelSupport} not  available"

def testSpacyNerModel(modelId, text):
    path = 'models/spacymodels/'+modelId+'/spacymodel'
    if os.path.isdir(path):
        predict = spacyModel.predict(path, text)
        return predict
    else: 
        return "Fail"


def testFlairNerModel(modelId, text):
    path = 'models/flairmodels/'+modelId+'/flairmodel/model.pt'
    if os.path.isfile(path):
        predict = flairModel.predict(path, text)
        return predict
    else: 
        return "Fail:  Model not found"

def testFlairClassifierModel(modelId, text):
    return "Flair Classifier Not Supported"

def testSpacyClassifierModel(modelId, text):
    return "Spacy ClassifierNot Supported"

## Train models
async def trainModel(modelId, tagId):
    ## Get More info about model
    trainData = await dataController.getEntityTagSetItems(tagId)
    model = await dataController.getModel(modelId)
    modelType = model["type"].upper()
    modelSupport = model["support"].upper()
    if modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.SPACY.name:
        return trainSpacyNerModel(modelId, trainData)
    elif modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        return trainFlairNerModel(modelId, trainData)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.SPACY.name:
        return "Model type {modelType} or Model support {modelSupport} not  available"
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        return "Model type {modelType} or Model support {modelSupport} not  available"
    else:
        return "Model type {modelType} or Model support {modelSupport} not  available"

def trainSpacyNerModel(modelId, trainData):
    path = 'models/spacymodels/'+modelId+'/spacymodel'
    data = prepareTrainData(trainData)
    if os.path.isdir(path):
        spacyModel.trainModel(path, data)
        return "training Done"
    else: 
        return "Fail"

def prepareTrainData(trainData):
    dataSet = []
    for item in trainData:
        dataSet.extend([(tags["text"], {"entities": [(tag["start"],tag["end"],tag["tag"]) for tag in tags["entities"]]}) for tags in item["tags"]])
    return dataSet
    
def trainFlairNerModel(modelId, trainData):
    path = 'models/flairmodels/'+modelId+'/flairmodel'
    modelfile = 'model.pt'
    data = prepareTrainData(trainData)
    if os.path.isdir(path):
        flairModel.trainModel(path, modelfile, data)
        return "training Done"
    else: 
        return "Fail: model not found"


# Labels  db
# raw db