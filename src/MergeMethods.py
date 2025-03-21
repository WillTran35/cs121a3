import json
import linecache
from collections import defaultdict, deque
from pathlib import Path
from task import Task
# from Final_Index import Final_Index
import heapq
from constants import indexDict, lengthIndexDict, countDict, indexOfIndexDict, DictIndex, num_docs, sortByFreq
import math

queue = deque()
def sortPartialIndex(partial_index):
    #  need to sort based on term
    #  then sort based on frequency
    index = {}
    for key, item in partial_index.items():
        index[key] = {x.getID(): x.getFrequencyOfToken(key) for x in item}

    sorted_index = dict(sorted(index.items(), key=lambda x: x[0]))
    # print(sorted_index)
    sorted_index2 = {key: dict(sorted(value.items(), key=lambda x: x[1], reverse=True)) for key, value in sorted_index.items()}
    # print(sorted_index2)
    return sorted_index2

def createNewPartialJson(count, partial_index):
    with open(f"jsonFolder/{count - 10000}-{count}.jsonl", "w") as f:
        # data = {}
        partial_index = sortPartialIndex(partial_index)
        for key, value in partial_index.items():
            # data = {"term": key, "index": {x.getID(): x.getFrequencyOfToken(key) for x in item}}
            data = {"term": key, "index": value}
            json.dump(data, f)
            f.write('\n')

def createNewDictPartialJson(count, dictList):
    with open(f"DictJsonFolder/{count - 10000}-{count}.jsonl", "w") as f:
        # data = {}
        for key, item in dictList.items():
            data = {key: item}
            json.dump(data, f)
            f.write('\n')


def createIndexOfIndexes(folder):
    count = 0

    for json_file in folder.rglob("*.jsonl"):
        # i want to create an index of indexes for each partial index, so when i merge, i look through
        # the index of indexes and get to the position in each partial index
        index = {}
        with open(json_file, "r", encoding="ascii") as f:
            print(json_file, countDict[str(json_file)])

            for line_num, line in enumerate(f, start=1):
                decoded_line = line.strip()
                print(line_num)
                if not decoded_line:
                    print("not decoded line")
                    continue

                data = json.loads(decoded_line)
                term = data["term"]
                index[term] = line_num

            with open(f"IndexOfIndexes/{countDict[str(json_file)]}-IndexOfIndexes.jsonl", "w") as a:
                for key, value in index.items():
                    data = {"term": key, "position":  value}
                    json.dump(data, a)
                    a.write('\n')
            # count += 1


def createFinalIndexOfIndexes():
    with open("finalIndex/final_IndexFINAL.jsonl", "r") as a,\
            open("IndexOfIndexes/final-IndexOfIndexes.jsonl", "w") as b:
        count = 1
        while True:
            line = a.readline()
            if not line:
                break
            term = json.loads(line)["term"]
            term_loc_dict = {"term": term, "position": count}
            json.dump(term_loc_dict, b)
            b.write('\n')
            count += 1


def getAllUniqueTerms(folder):
    terms = set()
    for json_file in folder.rglob("*.jsonl"):
        with open(json_file, "r") as f:
            for line in f:
                data = json.loads(line)
                terms.add(data["term"])

    return terms

def mergeList(fd):
    result = defaultdict()
    item = queue.popleft()
    term = item.getTerm()

    result.update(item.getIndex())

    while len(queue) > 1:
        item = queue.popleft()
        curr_term = item.getTerm()

        if term != curr_term:
            break

        result.update(item.getIndex())
    if queue:
        print(f"updated Index at {term}. This is term[0] = {queue[0]}")
        print("writing to file")
    result = sortByFreq(result)
    idf_score = math.log(num_docs / len(result))
    data = {"term": term, "index": result, "idf_score" : idf_score}

    json.dump(data, fd)
    fd.write("\n")
    print("finished writing to file")


def prioQ():
    with open(indexDict[0], "r") as a, open(indexDict[1], "r") as b, open(indexDict[2], "r") as c, \
            open(indexDict[3], "r") as d, open(indexDict[4], "r") as e, open(indexDict[5], "r") as f, \
            open(indexDict[6], "w") as g:

        file_des = [a, b, c, d, e, f]
        location = list(range(1, 7))
        result_q = set()

        q = []
        for file in file_des:
            jsonObj = json.loads(file.readline())
            term = jsonObj["term"]
            index = jsonObj["index"]
            position = file
            task = Task(term, index, position, file_des.index(position))
            q.append(task)

        print(location)
        print(f"intial: {q}")
        heapq.heapify(q)
        print(f"end: {q}")

        while q:
            task: Task = heapq.heappop(q)
            # print(task)
            term = task.getTerm()
            index = task.getIndex()
            location = task.getLocation()
            queue.append(task)
            result_q.add(term)  # add to result

            next = location.readline()
            if next != "":
                jsonObj = json.loads(next)
                term = jsonObj["term"]
                index = jsonObj["index"]
                location = location
                task = Task(term, index, location, file_des.index(location))
                heapq.heappush(q, task)

            if len(queue) > 1 and queue[0].getTerm() != queue[-1].getTerm():
                mergeList(g)

        if queue:
            mergeList(g)
        # print(len(result_q))

def mergeDict():
    with open(DictIndex[0], "r") as a, open(DictIndex[1], "r") as b, open(DictIndex[2], "r") as c, \
            open(DictIndex[3], "r") as d, open(DictIndex[4], "r") as e, open(DictIndex[5], "r") as f, \
            open(DictIndex[6], "w") as g:

        file_des = [a, b, c, d, e, f]
        count = 0
        for file in file_des:
            while True:
                line = file.readline()
                if not line:
                    break
                obj = json.loads(line)
                for key, value in obj.items():
                    doc = key
                    url = value
                data = {"Doc": doc, "URL": url}
                json.dump(data, g)
                g.write('\n')
                count += 1
    print(count)