import flairNLP.prepareDataset as prepareDataset
import flairNLP.trainModel as training


async def train():
    text = 'The new Dell Linux equipped laptop will also come with a Core i7 processor, 4GB of RAM, and a 256GB solid state drive, so DELL really isn’t messing around.'
    labels = 'Linux:OS, Core i7:PROCESSOR,Core i7 processor:PROCESSOR, Core:PROCESSOR, i7:PROCESSOR,4GB: SPECS,RAM: SPECS,256GB: SPECS,solid state drive:SPECS,processor:PROCESSOR, Dell:PRODUCT, solid:SPECS, state:SPECS, drive:SPECS'
    data = prepareDataset.prepareDatasets(text, labels)
    prepareDataset.writeDataSets('train/', 'train.txt', data)
    training.trainModels()
    return 'Success'

async def predict(text):
    predict = training.predict(text)
    return predict