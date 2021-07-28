import re
import os

def covertLabelsStrToList(labels: str):
    lst = [ele.replace('\n', '').strip() for ele in labels.split(",")]
    res = [tuple(ele.split(':')) for ele in lst]
    return res

def clean(text):
    '''
    Just a helper fuction to add a space before the punctuations for better tokenization
    '''
    filters = ["!", "#", "$", "%", "&", "(", ")", "/", "*", ".", ":", ";", "<", "=", ">", "?", "@", "[",
               "\\", "]", "_", "`", "{", "}", "~", "'", ","]
    for i in text:
        if i in filters:
            text = text.replace(i, ' '+ i)
        
    text.replace(u'\xa0', u' ')
    return text


def getWordsWithLabels(text, labelsList):
    for label in labelsList:
        subLabels = label[0].split(' ')
        for i, sublabel in enumerate(subLabels): 
            for find in re.finditer(sublabel, text, re.IGNORECASE):
                startIndex = find.start()
                ## update start index
                subText = text[find.start():]
                if re.search(sublabel, subText, re.IGNORECASE):
                    obj = re.findall(sublabel, subText, re.IGNORECASE)
                    startIndex = startIndex + subText.find(obj[0])
                    
                endIndex = startIndex + len(sublabel)
                ## ignore label tags <B->, <I->
                if startIndex >= 0 and not (startIndex >= 3 and text[endIndex]=='>' and text[startIndex - 3:startIndex]=="<I-" or text[startIndex - 3:startIndex]=="<B-"):
                    insertText = ""
                    if len(subLabels) > 1 and i > 0:
                        insertText = "<I-"+ label[1].strip() + ">"
                    else:
                        insertText = "<B-"+ label[1].strip() + ">"
                    if not (text[endIndex] == '<' and (text[endIndex+1] == 'B' or text[endIndex+1] == 'I')):
                        text = text[:endIndex]+ insertText + text[endIndex:]
                    else: 
                        print(sublabel, "has already tag")
    text.replace(u'\xa0', u' ') 
    finalList = []
    for tag in text.split(' '):
        tag.strip()
        if len(tag) > 0:
            endIndex = tag.find('<')
            if tag[endIndex] == '<' and (tag[endIndex+1] == 'B' or tag[endIndex+1] == 'I'):
                tag = tag[:endIndex]+ ' ' + tag[endIndex:].replace('>', '').replace('<','')
            else :
                tag = tag+ ' O'
            finalList.append(tag)
        
    return finalList


def prepareDatasets(text, labels):
    labelsList = covertLabelsStrToList(labels)
    text = clean(text)
    return getWordsWithLabels(text, labelsList)

def writeDataSets(filePath, fileName, list):
    if not os.path.isdir(filePath):
        os.makedirs (filePath)
    with open(filePath + fileName, 'w') as file:
        for i in list:
            file.writelines(i +'\n')
        file.writelines('\n')
