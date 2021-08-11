import spacy
import enum

 
class PreprocessingEnum(enum.Enum):
    STOPWORD = 1    #Stop words e.g ',' '.' 
    PUNCTUATION = 2     #Punctuations  e.g 'to', 'at'
    LAMMATIZE = 3   #Lammatization convert words form to base form e.g Killed -> Kill, Triggered -> Trigger
    JUNK = 4 #Unwanted words e.g "etc", "E.g", "i.g."


def executeProcessing(enums, doc):
    if PreprocessingEnum.LAMMATIZE.name in enums: 
        clean_doc = [token.lemma_ for token in doc if operations(enums, token)]
    else:
        clean_doc = [token.text for token in doc if operations(enums, token)]

    return ' '.join(clean_doc)

def operations(enums, token):
    # stop words
    if PreprocessingEnum.STOPWORD.name in enums: 
        stopWords = token.is_stop
    else:
        stopWords = False
    
    if PreprocessingEnum.PUNCTUATION.name in enums: 
        punct = token.is_punct
    else:
        punct = False
        
    if PreprocessingEnum.JUNK.name in enums: 
        junk = token.pos_=='X'
    else:
        junk = False

    return not stopWords and not punct and not junk

def startProcessing(processingEnums, textList):
    nlp = spacy.load("en_core_web_sm")
    updatedTextList = []
    for text in textList:
        doc = nlp(text)
        updatedTextList.append(executeProcessing(processingEnums, doc))
    return updatedTextList