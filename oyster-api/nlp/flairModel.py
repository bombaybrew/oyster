from flair.data import Corpus
from flair.datasets import ColumnCorpus, SentenceDataset
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings
from typing import List
from flair.trainers import ModelTrainer
from flair.models import SequenceTagger
from flair.data import Sentence
from shutil import copyfile
import os

def createModel(modelPath):
    # initializing the corpus
    trainDummy = SentenceDataset([Sentence('')])
    corpus: Corpus = Corpus(train=trainDummy, test=trainDummy, dev=trainDummy)
    tagger = getTagger(corpus)
    file = modelPath+'/blankmodel.pt'                          
    tagger.save(file)

def getTagger(corpus):
    tag_dictionary = corpus.make_tag_dictionary(tag_type='ner')                        
    embedding_types : List[TokenEmbeddings] = [
    WordEmbeddings('glove'),
    ## other embeddings
    ]
    embeddings : StackedEmbeddings = StackedEmbeddings(
                             embeddings=embedding_types)
    tagger : SequenceTagger = SequenceTagger(hidden_size=256,
                               embeddings=embeddings,
                               tag_dictionary=tag_dictionary,
                               tag_type='ner',
                               use_crf=True)
    return tagger

def getSentences(trainData):
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
            s1[tag[0]].add_tag('ner', tag[1])
        sentences.append(s1)
    
    return sentences

def trainModel(path, modelfile, trainData):
    ## divide data into train and test
    sentenceList = getSentences(trainData)
    trainlen = round(len(sentenceList)*0.80)
    TRAIN_DATA = SentenceDataset(sentenceList[:trainlen])
    TEST_DATA = SentenceDataset(sentenceList[trainlen:])

    # initializing the corpus
    corpus: Corpus = Corpus(train=TRAIN_DATA, test=TEST_DATA)

    if os.path.isfile(path+'/'+modelfile):
        tagger = SequenceTagger.load(path+'/'+ modelfile)
    else:
        tagger = getTagger(corpus)

    trainer : ModelTrainer = ModelTrainer(tagger, corpus)
    trainer.train(path+'/trained',
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=50)
    ## copy model to main folder
    copyfile(path+'/trained/final-model.pt', path+'/model.pt')
            

def predict(modelPath, text): 
    model = SequenceTagger.load(modelPath)
        # create example sentence
    sentence = Sentence(text)
    # predict the tags
    model.predict(sentence)
    return sentence.to_tagged_string()
