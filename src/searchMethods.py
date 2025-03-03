import json
import linecache
from collections import defaultdict

from constants import indexDict, lengthIndexDict, countDict, indexOfIndexDict, tokenizeline
from nltk.stem import PorterStemmer

def getPosition(target, index):
    #  {"term": "chichiest", "position": 773775}
    length = len(target)
    start = 1
    end = lengthIndexDict[index]  # length of index of index

    while start <= end:
        mid = (start + end) // 2
        line = linecache.getline(indexDict[index], mid)
        final = line.find('"', 10)
        # {"term": "mastelski", "index": {"Doc26472": 1}}
        substr = line[10: final]
        # print(f"substr: {substr}")
        if substr == target:
            position = json.loads(line)["position"]
            return position
        if substr > target:
            end = mid - 1
        else:
            start = mid + 1

    return -1


def getItem(line):
    target = linecache.getline(indexDict[6], line)
    obj = json.loads(target)["index"]
    result = []
    for i in obj.keys():
        result.append((i, obj[i]))
    # print(result)
    return result


def getAllPositionsOfWord(word):
    with open(indexDict[6], "r") as r, \
            open(indexDict[7], "r") as w:

        final_index_pos = getPosition(word, 7)
        print(f"position of {word}: {final_index_pos}")
        if final_index_pos != -1:
            # print(f"item of {word}: {getItem(final_index_pos)}")
            return getItem(final_index_pos)
        return -1

def querySearch(query):
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(i) for i in tokenizeline(query)]
    print(f"stemmed: {stemmed_tokens}")
    result = {}
    for i in stemmed_tokens:
        if i not in result:
            result[i] = getAllPositionsOfWord(i)
        else:
            result[i] += getAllPositionsOfWord(i)
    # print(result)
    x = andDocs(result)
    if x:
        return x
    return -1

def getValues(docList, doc):
    result = []
    print(docList)
    for key in docList.keys():
        result.append((key, docList[key][doc]))
    return result

def andDocs(docList):
    intersect = []
    for i in docList.values():
        x = set()
        for j in i:
            x.add(j[0])
        if x:
            intersect.append(x)
    intersection = set.intersection(*intersect)
    # print(len(intersection))
    for key in docList.keys():
        docList[key] = [i for i in docList[key] if i[0] in intersection]

    return docList

def rankDocs():
    # tf score is found at the index
    # calculate ldf score by log(total docs / num of docs containing word)
    pass


if __name__ == "__main__":
    # print(getPosition("master", 7))
    print(len(querySearch("cristina lopes")["cristina"]))