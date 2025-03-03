import json
import linecache
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
    return obj


def getAllPositionsOfWord(word):
    result = []
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
    result = list(getAllPositionsOfWord(i) for i in stemmed_tokens)
    # result_sorted = sorted(result, key=lambda x: len(x[0]))w
    x = andDocs(result)
    # print(x)
    if x:
        print(f"got intersections: {x}")
        return x
    return -1
    # print(result)
#

def andDocs(docList):
    dictSet = [set(i.keys()) for i in docList]
    intersect = set.intersection(*dictSet)


    return intersect
def findSameDocs():
    pass

if __name__ == "__main__":
    # print(getPosition("master", 7))
    querySearch("cristina lopes")