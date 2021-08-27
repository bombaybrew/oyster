# import nlp.prepareDataset as prepareDataset
from nlp.flairModel import FlairNERModel, FlairClassifierModel
import api.modelDataController as dataController
import api.dataSetController as dataSetController
import os.path
import os
from nlp.spacyModel import SpacyNERModel, SpacyClassifierModel
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
    categories = [] # TODO remove this hardcode
    if modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.SPACY.name:
        createSpacyNerModel(modelId)
    elif modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        createFlairNerModel(modelId)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.SPACY.name:
        createSpacyClassifierModel(modelId, categories)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        createFlairClassifierModel(modelId)
    else:
        return "Model type {modelType} or Model support {modelSupport} not  available"
    return "Success"

## Create Model methods
def createSpacyNerModel(modelId):
    path = 'models/spacymodels/'+modelId+'/spacymodel'
    os.chmod('models',0o777) 
    os.makedirs(path)
    SpacyNERModel(id=modelId, path=path).createModel()

def createSpacyClassifierModel(modelId, categories):
    path = 'models/spacymodels/'+modelId+'/classifiermodel'
    os.chmod('models',0o777) 
    os.makedirs(path)
    SpacyClassifierModel(id=modelId, path=path).createModel(categories)


def createFlairNerModel(modelId):
    path = 'models/flairmodels/'+modelId+'/flairmodel'
    modelfile = 'model.pt'
    os.chmod('models',0o777) 
    os.makedirs(path)
    FlairNERModel(id=modelId, path=path, fileName=modelfile).createModel()


def createFlairClassifierModel(modelId):
    path = 'models/flairmodels/'+modelId+'/classifiermodel'
    modelfile = 'classifier_model.pt'
    os.chmod('models',0o777) 
    os.makedirs(path)
    FlairClassifierModel(id=modelId, path=path, fileName=modelfile).createModel()


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
        predict = SpacyNERModel(id=modelId, path=path).predict(text)
        return predict
    else: 
        return "Fail:  Model not found"


def testFlairNerModel(modelId, text):
    path = 'models/flairmodels/'+modelId+'/flairmodel'
    modelfile = 'model.pt'
    if os.path.isfile(path+'/'+modelfile):
        predict = FlairNERModel(id=modelId, path=path, fileName=modelfile).predict(text)
        return predict
    else: 
        return "Fail:  Model not found"

def testSpacyClassifierModel(modelId, text):
    path = 'models/spacymodels/'+modelId+'/classifiermodel'
    if os.path.isdir(path):
        predict = SpacyClassifierModel(id=modelId, path=path).predict(text)
        return predict
    else: 
        return "Fail:  Model not found"

def testFlairClassifierModel(modelId, text):
    path = 'models/flairmodels/'+modelId+'/classifiermodel'
    modelfile = 'classifier_model.pt'
    if os.path.isfile(path+'/'+modelfile):
        predict = FlairClassifierModel(id=modelId, path=path, fileName=modelfile).predict(text)
        return predict
    else: 
        return "Fail:  Model not found"

## Train models
async def trainModel(modelId, tagId):
    ## Get More info about model
    trainData = await dataSetController.getEntityTagSetItems(tagId)
    model = await dataController.getModel(modelId)
    modelType = model["type"].upper()
    modelSupport = model["support"].upper()
    if modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.SPACY.name:
        return trainSpacyNerModel(modelId, trainData)
    elif modelType == ModelTpyeEnum.NER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        return trainFlairNerModel(modelId, trainData)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.SPACY.name:
        return trainSpacyClassifierModel(modelId, trainData)
    elif modelType == ModelTpyeEnum.CLASSIFIER.name and modelSupport == ModelSupportEnum.FLAIR.name:
        return trainFlairClassifierModel(modelId, trainData)
    else:
        return "Model type {modelType} or Model support {modelSupport} not  available"

def trainSpacyNerModel(modelId, trainData):
    path = 'models/spacymodels/'+modelId+'/spacymodel'
    data = prepareTrainData(trainData)
    if os.path.isdir(path):
        SpacyNERModel(id=modelId, path=path).trainModel(data)
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
        FlairNERModel(id=modelId, path=path, fileName=modelfile).trainModel(data)
        return "training Done"
    else: 
        return "Fail: model not found"


## Classifier Models
def trainSpacyClassifierModel(modelId, trainData):
    path = 'models/spacymodels/'+modelId+'/classifiermodel'
    data = prepareTrainDataClassifier(trainData)
    if os.path.isdir(path):
        SpacyClassifierModel(id=modelId, path=path).trainModel(data)
        return "training Done"
    else: 
        return "Fail"

def trainFlairClassifierModel(modelId, trainData):
    path = 'models/flairmodels/'+modelId+'/classifiermodel'
    modelfile = 'classifier_model.pt'
    data = prepareTrainDataClassifier(trainData)
    if os.path.isdir(path):
        FlairClassifierModel(id=modelId, path=path, fileName=modelfile).trainModel(data)
        return "training Done"
    else: 
        return "Fail: model not found"

def prepareTrainDataClassifier(trainData):
    dataSet = []
    for item in trainData:
        dataSet.extend([label for label in item["tags"]])
    return dataSet


# Labels  db
# raw db