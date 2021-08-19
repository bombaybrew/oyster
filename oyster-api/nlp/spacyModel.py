import spacy
from spacy.util import minibatch, compounding
import random
from spacy.training import Example

def createModel(modelPath):
    nlpBlank=spacy.blank("en")
    nlpBlank.add_pipe('ner')
    nlpBlank.to_disk(modelPath)


def trainModel(modelPath, trainData):
    TRAIN_DATA = trainData
    nlp=spacy.load(modelPath) 
    # Getting the ner component
    ner=nlp.get_pipe('ner')
    nlp.begin_training()
    # Resume training
    optimizer = nlp.resume_training()
    move_names = list(ner.move_names)
    # List of pipes you want to train
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    # List of pipes which should remain unaffected in training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    # Begin training by disabling other pipeline components
    with nlp.disable_pipes(*other_pipes) :
        sizes = compounding(1.0, 4.0, 1.001)
        # Training for 30 iterations     
        for itn in range(30):
            # shuffle examples before training
            random.shuffle(TRAIN_DATA)
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=sizes)
            # ictionary to store losses
            losses = {}
            for batch in batches:
                texts, annotations = batch[0]
                doc = nlp.make_doc(texts)
                example = Example.from_dict(doc, annotations)
                # Calling update() over the iteration
                nlp.update([example], sgd=optimizer, drop=0.35, losses=losses)
    
    ## Save model
    nlp.to_disk(modelPath)


def predict(modelPath, text): 
    nlp = spacy.load(modelPath)
    doc = nlp(text)
    list = []
    for ent in doc.ents:
        list.append({ent.text, ent.label_})
    return list