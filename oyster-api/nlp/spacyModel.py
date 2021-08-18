import spacy

def predict(modelPath, text): 
    nlp = spacy.load(modelPath)
    doc = nlp(text)
    list = []
    for ent in doc.ents:
        list.append({ent.text, ent.label_})
    return list