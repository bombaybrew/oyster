from nlp.nlpModel import NlpModel, BLANK_MODEL, TAG_NER_TYPE
from flair.data import Corpus
from flair.datasets import ColumnCorpus, SentenceDataset
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, DocumentRNNEmbeddings
from typing import List
from flair.trainers import ModelTrainer
from flair.models import SequenceTagger, TextClassifier
from flair.data import Sentence
from shutil import copyfile
import os


class FlairNERModel(NlpModel):
    def createModel(self):
        """
        Create Ner Tagger model 
        return: NONE
        """
        # initializing the corpus
        trainDummy = SentenceDataset([Sentence('')])
        corpus: Corpus = Corpus(train=trainDummy, test=trainDummy, dev=trainDummy)
        tagger = self.getTagger(corpus)
        file = self.path+'/' + BLANK_MODEL                         
        tagger.save(file)

    def getTagger(self, corpus):
        tag_dictionary = corpus.make_tag_dictionary(tag_type=TAG_NER_TYPE)                        
        embedding_types : List[TokenEmbeddings] = [
        WordEmbeddings('glove'),
        ## other embeddings
        ]
        embeddings : StackedEmbeddings = StackedEmbeddings(
                                embeddings=embedding_types)
        tagger : SequenceTagger = SequenceTagger(hidden_size=256,
                                embeddings=embeddings,
                                tag_dictionary=tag_dictionary,
                                tag_type=TAG_NER_TYPE,
                                use_crf=True)
        return tagger

    def getSentences(self, trainData):
        sentences = []
        for data in trainData: 
            s1 = Sentence(data[0])
            text = data[0]
            entities = data[1]['entities']
            taglist = []
            for item in entities:
                subtext = text[item[0]:item[1]].split()
                startIndex = len(text[:item[0]].split())
                for i, t in enumerate(subtext):
                    if i > 0:
                        tag = (i+startIndex, 'I-'+item[2])
                        taglist.append(tag)
                    else:
                        tag = (startIndex, 'B-'+item[2])
                        taglist.append(tag)

            for tag in taglist:
                s1[tag[0]].add_tag(TAG_NER_TYPE, tag[1])
            sentences.append(s1)
        
        return sentences

    def trainModel(self, trainData):
        """
        Train NER model
        trainData (list): List of train data in below foramt
        [("Pizza is a common fast food.", {"entities": [(0, 5, "FOOD")]})]
     
        after train it will save mode at 
        Location: path
        """
        ## divide data into train and test
        sentenceList = self.getSentences(trainData)
        trainlen = round(len(sentenceList)*0.80)
        TRAIN_DATA = SentenceDataset(sentenceList[:trainlen])
        TEST_DATA = SentenceDataset(sentenceList[trainlen:])

        # initializing the corpus
        corpus: Corpus = Corpus(train=TRAIN_DATA, test=TEST_DATA)
        taggerFile = self.path+'/'+self.fileName
        if os.path.isfile(taggerFile):
            tagger = SequenceTagger.load(taggerFile)
        else:
            tagger = self.getTagger(corpus)

        trainer : ModelTrainer = ModelTrainer(tagger, corpus)
        trainer.train(self.path+'/trained',
                learning_rate=0.1,
                mini_batch_size=32,
                max_epochs=50)
        ## copy model to main folder
        copyfile(self.path+'/trained/final-model.pt', taggerFile)
                

    def predict(self, text): 
        """
        Predict model output for given text
        text (str): Any text
        return : text with label
        text: I <B-Person> Like Maggi <B-FOOD>
        """
        model = SequenceTagger.load(self.path+'/'+self.fileName)
            # create example sentence
        sentence = Sentence(text)
        # predict the tags
        model.predict(sentence)
        return sentence.to_tagged_string()


class FlairClassifierModel(NlpModel):
    def createModel(self):
        """
        Create Classifier model 
        return: NONE
        """
        # initializing the corpus
        trainDummy = SentenceDataset([Sentence('')])
        corpus: Corpus = Corpus(train=trainDummy, test=trainDummy, dev=trainDummy)
        tagger = self.getClassifier(corpus)
        file = self.path+'/' + BLANK_MODEL                         
        tagger.save(file)

    def getClassifier(self, corpus):
        label_dict = corpus.make_label_dictionary()                        
        embedding_types : List[TokenEmbeddings] = [
        WordEmbeddings('glove'),
        ## other embeddings
        ]
        # Can choose between many RNN types (GRU by default, to change use rnn_type parameter)
        document_embeddings = DocumentRNNEmbeddings(embedding_types, hidden_size=256)
        # 5. create the text classifier
        classifier = TextClassifier(document_embeddings, label_dictionary=label_dict)
        return classifier

    def getSentences(self, trainData):
        sentences = []
        for data in trainData:
            text = data['text']
            label = data['label']
            s1 = Sentence(text)
            s1.add_label('cat', label)
            sentences.append(s1)

        return sentences

    def trainModel(self, trainData):
        """
        Train Classifier Model
        trainData (list): List of text and label
        expecting train data in this format: 
        [{"label": "CRIME", "text": "Any Text"}]

        It will train predefine model or create new if required
        after train it will save mode at 
        Location: path+'/'+fileName
        """
        ## divide data into train and test
        sentenceList = self.getSentences(trainData)
        trainlen = round(len(sentenceList)*0.80)
        TRAIN_DATA = SentenceDataset(sentenceList[:trainlen])
        TEST_DATA = SentenceDataset(sentenceList[trainlen:])

        # initializing the corpus
        corpus: Corpus = Corpus(train=TRAIN_DATA, test=TEST_DATA)
        modelFile = self.path+'/'+self.fileName
        if os.path.isfile(modelFile):
            model = TextClassifier.load(modelFile)
        else:
            model = self.getClassifier(corpus)

        trainer : ModelTrainer = ModelTrainer(model, corpus)
        trainer.train(self.path+'/trained',
                learning_rate=0.1,
                mini_batch_size=32,
                anneal_factor=0.5,
                patience=5,
                max_epochs=50)
        ## copy model to main folder
        copyfile(self.path+'/trained/final-model.pt', modelFile)
                

    def predict(self, text): 
        """
        Predict model output for given text
        text (str): Any text
        return : categories with confindecs score
        [Label (score)]
        {'Cat1': 0.9, 'Cat2': 0.2}
        """
        model = TextClassifier.load(self.path+'/'+self.fileName)
            # create example sentence
        sentence = Sentence(text)
        # predict the tags
        model.predict(sentence)
        out = {}
        for label in sentence.labels:
            out[label.value] =label.score
        return out

