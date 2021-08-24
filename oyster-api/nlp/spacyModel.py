from numpy.lib.function_base import select
from nlp.nlpModel import NlpModel, TAG_NER_TYPE, CLASSIFIER_TYPE
import spacy
from spacy.util import minibatch, compounding
import random
from spacy.training import Example

class SpacyNERModel(NlpModel):
    def createModel(self):
        """
        Create Ner Tagger model 
        return: NONE
        """
        nlpBlank=spacy.blank("en")
        nlpBlank.add_pipe(TAG_NER_TYPE)
        nlpBlank.to_disk(self.path)


    def trainModel(self, trainData):
        """
        Train NER model
        trainData (list): List of train data in below foramt
        [("Pizza is a common fast food.", {"entities": [(0, 5, "FOOD")]})]
     
        after train it will save mode at 
        Location: path
        """
        TRAIN_DATA = trainData
        nlp=spacy.load(self.path) 
        nlp.begin_training()
        # Resume training
        optimizer = nlp.resume_training()
        # List of pipes you want to train
        pipe_exceptions = [TAG_NER_TYPE, "trf_wordpiecer", "trf_tok2vec"]
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
        nlp.to_disk(self.path)


    def predict(self, text): 
        """
        Predict model output for given text
        text (str): Any text
        return : text with label
        [{'text', 'label'}]
        """
        nlp = spacy.load(self.path)
        doc = nlp(text)
        list = []
        for ent in doc.ents:
            list.append({ent.text, ent.label_})
        return list



class SpacyClassifierModel(NlpModel):
    def createModel(self, categories=[]):
        """
        Create Classifier model with categories
        categories (list): List of categories

        return: List of Labels
        """
        nlpBlank=spacy.blank("en")
        nlpBlank.add_pipe(CLASSIFIER_TYPE)
        # Adding the labels to textcat
        textcat = nlpBlank.get_pipe(CLASSIFIER_TYPE)
        for cat in categories:
            textcat.add_label(cat)
        nlpBlank.to_disk(self.path)
        return textcat.labels

    def getCateogories(self, data):
        return set([item['label'] for item in data])

    def prepareData(self, trainData, allCats):
        data = []
        for item in trainData:
            cat = item['label']
            value = {}
            for lb in allCats:
                if (cat == lb):
                    value[lb] = 1
                else:
                    value[lb] = 0
            item  = (item['text'], {'cats': value})
            data.append(item)
        return data

    def trainModel(self, trainData):
        """
        Train Classifier model
        trainData (list): List of train data in below foramt
        [('Review or Text or sentence',{'cats': {'Category1': 0, 'Category2': 1}})]
     
        after train it will save mode at 
        Location: path
        """
        allCats = self.getCateogories(trainData)
        TRAIN_DATA = self.prepareData(trainData, allCats)
        nlp=spacy.load(self.path) 
        # Adding the labels to textcat
        textcat = nlp.get_pipe(CLASSIFIER_TYPE)
        for cat in allCats:
            textcat.add_label(cat)
        
        # Disabling other components
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != CLASSIFIER_TYPE]
        with nlp.disable_pipes(*other_pipes):  # only train textcat
            optimizer = nlp.begin_training()
            # Performing training
            for i in range(30):
                losses = {}
                batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = batch[0]
                    doc = nlp.make_doc(texts)
                    example = Example.from_dict(doc, annotations)
                    nlp.update([example], sgd=optimizer, drop=0.2,
                            losses=losses)
        ## Save model
        nlp.to_disk(self.path)


    def predict(self, text): 
        """
        Predict model output for given text
        text (str): Any text
        return : categories with confindecs score
        {'Cat1': 0.9, 'Cat2': 0.2}
        """
        nlp = spacy.load(self.path)
        doc = nlp(text)
        return doc.cats
