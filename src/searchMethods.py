import json
from constants import indexDict, lengthIndexDict, countDict, indexOfIndexDict, tokenizeline
from nltk.stem import PorterStemmer
import time
from ranking import computeTF_IDFscore
from MergeMethods import sortByFreq
def convertToTxt():
    with open("finalIndex/final_IndexFINAL.jsonl", "r") as f, open("finalIndex/final.txt", "w") as w:
        while True:
            line = f.readline()
            if not line:
                break
            obj = json.loads(line)
            term = obj["term"]
            index = obj["index"]
            idf_score = obj["idf_score"]
            w.write(f'"term": \"{term}\", "index": {index}, "idf_score": {idf_score}\n')

def convertDictJsonToTxt():
    with open("DictJsonFolder/final_IndexFINAL.jsonl", "r") as f, open("DictJsonFolder/final_dict.txt", "w") as w:
        while True:
            line = f.readline()
            if not line:
                break
            obj = json.loads(line)
            doc = obj["Doc"]
            index = obj["URL"]
            w.write(f'{doc}|{index}\n')

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

def parsePositionFromLine(line):
    """Parses "position" part from line."""
    start = line.find('position": ')
    end = line.find('\n')
    return line[start + 11:end]

def getStartEnd(word):
    """Returns start of skip list and end of skip list. Using the start and end, we can seek to the start and only read
    to the end position of final index file."""
    with open(f"SkipLists/{word[0]}_skiplist.txt", "r") as r:
        prev = 0
        while True:
            line = r.readline()
            if not line:
                break
            term = line[0:line.find('|')]
            pos_start = line.find('|') + 1
            pos_end = line.find('\n')
            position = int(line[pos_start:pos_end])
            if word > term:
                prev = position
            elif word <= term:
                return prev, position

def parseIndexFromLine(line) :
    start = line.find('{')
    end = line.find('}') + 1
    # print(line[start:end])
    return line[start:end]

def parseIDFscore(line):
#     {"term": "cristoforo", "index": {"Doc46591": 5.101405743366643e-07}, "idf_score": 10.922208510961449}
    first = line.find("|")
    start = line.find("|", first + 1)
    end = line.find("\n")
    return line[start + 1:end]

def parseIndex(line):
    new = line[1:-1]
    splitted = new.split(", ")

    docids = {}
    for i in splitted:
        doc = i.split(":")[0][1:-1]
        end = i.split(":")[1][:i.split(":")[1].find('}')]
        freq = float(end)
        docids[doc] = freq

    return docids

def findWordIndex(word):
    with open(f"Indexes/{word[0]}_index.txt", "r") as r:
        start_end = getStartEnd(word)
        start, end = start_end[0], start_end[1]
        # print("IM HEREE", start, end)
        r.seek(start)
        while r.tell() != end:
            line = r.readline()
            if not line:
                break
            final = line.find("|")
            term = line[0:final]
            # print("hello" , term)
            # print(term)
            if term == word:
                index = parseIndex(line)
                idf_score = parseIDFscore(line)
                return index, float(idf_score)

def querySearch(query):
    start = time.time()
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(i) for i in tokenizeline(query)]
    print(f"stemmed: {stemmed_tokens}")
    result = {}
    idf_scores = {}
    for i in stemmed_tokens:
        index, idf_score = findWordIndex(i)[0], findWordIndex(i)[1]
        if i not in result:
            result[i] = index
        else:
            result[i].update(index)

        idf_scores[i] = idf_score
    # print(idf_scores)
    # print (result)
    x = andDocs(result, idf_scores,start)
    if x:
        return x
    return -1


def andDocs(docList, idf_scores, start):
    intersect = []
    # print(docList)

    for key, value in docList.items():
        intersect.append(set(value))

    intersection = set.intersection(*intersect)
    # print(f"INTERSECTION {intersection}")
    # print(len(intersection))
    for key in docList.keys():
        # print(docList[key])
        docList[key] = {i: docList[key][i] for i in docList[key] if i in intersection}
    # print(docList)
    end = time.time()
    print(end - start)
    result = computeTF_IDFscore(intersection, docList, idf_scores)
    return result

def run():
    convertToTxt()
    createIndexOfIndexesTxt()

if __name__ == "__main__":

    result = querySearch("hello bitch how are you doing im in the bay")
    print(result)
    # print(len(result["machin"]))
    # # # print(result["lope"], len(result["cristina"]))
    end = time.time()
    # print(end-start)
    #

