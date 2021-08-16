# import nlp.prepareDataset as prepareDataset
import nlp.flairModel as flairModel
import api.dataController as dataController
import os.path

async def testModel(modelId, text):
    path = 'models/'+modelId+'/final-model.pt'
    if os.path.isfile(path):
        ## Get More info about model
        model = await dataController.getModel(modelId)
        model = model[0]
        predict = flairModel.predict(path, text)
        return predict
    else: 
        return "Fail"

async def trainModel():
    return 'Success'

# Labels  db
# raw db