# import nlp.prepareDataset as prepareDataset
import nlp.flairModel as flairModel
import api.dataController as dataController
import os.path
import nlp.spacyModel as spacyModel
import enum

class ModelSupportEnum(enum.Enum):
    SPACY = 1
    FLAIR = 2

class ModelTpyeEnum(enum.Enum):
    NER = 1
    CLASSIFIER = 2
    
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
    path = 'models/spacymodels/'+modelId+'/models'
    if os.path.isdir(path):
        predict = spacyModel.predict(path, text)
        return predict
    else: 
        return "Fail"


def testFlairNerModel(modelId, text):
    path = 'models/flairmodels/'+modelId+'/model.pt'
    if os.path.isfile(path):
        predict = flairModel.predict(path, text)
        return predict
    else: 
        return "Fail"

def testFlairClassifierModel(modelId, text):
    return "Flair Classifier Not Supported"

def testSpacyClassifierModel(modelId, text):
    return "Spacy ClassifierNot Supported"

async def trainModel():
    return 'Success'

# Labels  db
# raw db