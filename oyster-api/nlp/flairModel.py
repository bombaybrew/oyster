from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings
from typing import List
from flair.trainers import ModelTrainer
from flair.models import SequenceTagger
from flair.data import Sentence


def trainModel():
    # define columns
    columns = {0 : 'text', 1 : 'ner'}
    # directory where the data resides
    data_folder = 'train'
    # initializing the corpus
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file = 'train.txt',
                              test_file = 'train.txt',
                              dev_file = 'train.txt')

    # tag to predict
    tag_type = 'ner'
    # make tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

    embedding_types : List[TokenEmbeddings] = [
        WordEmbeddings('glove'),
        ## other embeddings
        ]
    embeddings : StackedEmbeddings = StackedEmbeddings(
                                 embeddings=embedding_types)

                                
    tagger : SequenceTagger = SequenceTagger(hidden_size=256,
                                       embeddings=embeddings,
                                       tag_dictionary=tag_dictionary,
                                       tag_type=tag_type,
                                       use_crf=True)

    trainer : ModelTrainer = ModelTrainer(tagger, corpus)
    trainer.train('resources/taggers',
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=150)
            

def predict(modelPath, text): 
    model = SequenceTagger.load(modelPath)
        # create example sentence
    sentence = Sentence(text)
    # predict the tags
    model.predict(sentence)
    return sentence.to_tagged_string()
