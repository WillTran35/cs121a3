import json
import linecache
from constants import indexDict, lengthIndexDict, countDict, indexOfIndexDict
def getPosition(target, index):
    #  {"term": "chichiest", "position": 773775}
    length = len(target)
    start = 1
    end = lengthIndexDict[index]  # length of index of index

    while start < end:
        mid = (start + end) // 2
        line = linecache.getline(indexDict[index], mid)
        substr = line[10: length + 10]
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
        if final_index_pos != -1:
            return getItem(final_index_pos)
        return -1

def findSameDocs():
    pass

