import json
# import linecache
from collections import defaultdict
import ast
from constants import indexDict, lengthIndexDict, countDict, indexOfIndexDict, tokenizeline
from nltk.stem import PorterStemmer
import time


def convertToTxt():
    with open("finalIndex/final_IndexFINAL.jsonl", "r") as f, open("finalIndex/final.txt", "w") as w:
        while True:
            line = f.readline()
            if not line:
                break
            obj = json.loads(line)
            term = obj["term"]
            index = obj["index"]
            w.write(f'"term": \"{term}\", "index": {index}\n')

def createIndexOfIndexesTxt():
    with open("finalIndex/final.txt", "r") as f, open("IndexOfIndexes/final.txt", "w") as w:
        count = 1
        while True:
            line = f.readline()
            if not line:
                break
            end = line.find('"', 9)
            term = line[9:end]
            print(term)
            w.write(f'"term": \"{term}\", "position": {count}\n')
            count += 1

def binarySearch(word):
    """Binary search to find line number."""
    mylist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
              'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    first = word[0]
    start = 0
    end = len(mylist)
    while start <= end:
        mid = (start + end) // 2
        if mylist[mid] == first:
            return mid
        elif mylist[mid] < first:
            start = mid + 1
        else:
            end = mid - 1
    return -1

def parsePositionFromLine(line):
    """Parses "position" part from line."""
    start = line.find('position": ')
    end = line.find('\n')
    return line[start + 11:end]

def getStartEnd(word):
    """Returns start of skip list and end of skip list. Using the start and end, we can seek to the start and only read
    to the end position of final index file."""
    position = binarySearch(word)
    if position < 0:
        return None

    with open("IndexOfIndexes/bytes.txt", "r") as r:
        count = 0
        result = []
        while count < position:
            line = r.readline()
            count += 1
        line = r.readline()
        result.append(int(parsePositionFromLine(line)))
        # print(line, int(parsePositionFromLine(line)))
        line = r.readline()
        result.append(int(parsePositionFromLine(line)))
        # print(line, int(parsePositionFromLine(line)))
        return result

def parseIndexFromLine(line) -> dict:
    start = line.find('{')
    end = line.find('\n')
    return line[start:end]

def findWordIndex(word):
    with open("finalIndex/final.txt", "r") as r:
        start_end = getStartEnd(word)
        start, end = start_end[0], start_end[1]

        r.seek(start)
        while r.tell() != end:
            line = r.readline()
            if not line:
                break
            end = line.find('"', 9)
            term = line[9:end]
            if term == word:
                index = parseIndexFromLine(line)
                return ast.literal_eval(index)

def createByteIndex():
    with open(indexDict[9], "r") as r, open("IndexOfIndexes/bytes.txt", "w") as w:
        mydict = {}
        while True:
            pos = r.tell()
            line = r.readline()
            if not line:
                break
            start = line.find('"', 8) + 1
            end = line.find('"', start)
            term = line[start:end]
            char = term[0]
            if char not in mydict:
                mydict[char] = pos  # byte position
                w.write(f'"char": {char}, "position": {pos}\n')


def querySearch(query):
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(i) for i in tokenizeline(query)]
    print(f"stemmed: {stemmed_tokens}")
    result = {}
    for i in stemmed_tokens:
        if i not in result:
            result[i] = findWordIndex(i)
        else:
            result[i] += findWordIndex(i)
    # return (result)
    x = andDocs(result)
    if x:
        return x
    return -1


def andDocs(docList):
    intersect = []
    for key, value in docList.items():
        intersect.append(set(value))

    intersection = set.intersection(*intersect)
    # print(f"INTERSECTION {intersection}")
    # print(len(intersection))
    for key in docList.keys():
        docList[key] = [i for i in docList[key] if i in intersection]

    return docList

def run():
    convertToTxt()
    createIndexOfIndexesTxt()
    createByteIndex()

if __name__ == "__main__":
    run()
    start = time.time()
    # createByteIndex()
    result = querySearch("master of software engineering")
    # print(result)
    # print(result["lope"], len(result["cristina"]))
    end = time.time()
    print(end-start)
    #

