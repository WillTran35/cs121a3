import json
import linecache
indexDict = {0: "jsonFolder/0-10000.jsonl", 1: "jsonFolder/10000-20000.jsonl",
             2: "jsonFolder/20000-30000.jsonl", 3: "jsonFolder/30000-40000.jsonl",
             4: "jsonFolder/40000-50000.jsonl", 5: "jsonFolder/45393-55393.jsonl"}

countDict = {"jsonFolder/0-10000.jsonl": 0, "jsonFolder/10000-20000.jsonl": 1,
            "jsonFolder/20000-30000.jsonl": 2, "jsonFolder/30000-40000.jsonl": 3,
             "jsonFolder/40000-50000.jsonl": 4, "jsonFolder/45393-55393.jsonl": 5}

indexOfIndexDict = {"IndexOfIndexes/0-IndexOfIndexes.jsonl": 0, "IndexOfIndexes/1-IndexOfIndexes.jsonl": 1,
                    "IndexOfIndexes/2-IndexOfIndexes.jsonl": 2, "IndexOfIndexes/3-IndexOfIndexes.jsonl": 3,
                    "IndexOfIndexes/4-IndexOfIndexes.jsonl": 4, "IndexOfIndexes/5-IndexOfIndexes.jsonl": 5}
def sortPartialIndex(partial_index):
    #  need to sort based on term
    #  then sort based on frequency
    index = {}
    for key, item in partial_index.items():
        index[key] = {x.getID(): x.getFrequencyOfToken(key) for x in item}

    sorted_index = dict(sorted(index.items(), key = lambda x : x[0]))
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




def findAllValues(folder, target):
    result = {}
    for json_file in folder.rglob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)
            if target in data:
                if target not in result:
                    result[target] = data[target]
                else:
                    result[target].update(data[target])

    result[target] = dict(sorted(result[target].items(), key = lambda item: item[1], reverse=True))
    print(result)
    return result

def getAllUniqueTerms(folder):
    terms = set()
    for json_file in folder.rglob("*.jsonl"):
        with open(json_file, "r") as f:
            for line in f:
                data = json.loads(line)
                terms.add(data["term"])

    return terms

def getAllPositionsOfWord(folder, word):
    result = []
    for json_file in folder.rglob("*.jsonl"):
        # print(json_file)
        with open(json_file, "r") as f:
            for line in f:
                data = json.loads(line)
                if data["term"] == word.casefold():
                    # print(data["term"], data["position"])
                    result.append((indexOfIndexDict[str(json_file)], data["position"]))
                    # print("got one")
                    break

    return result

def returnJsonObjectAtPos(file_num, position):
    with open(indexDict[file_num], "rb") as w:
        line = linecache.getline(indexDict[file_num], position).strip()
        print(line)
        return json.loads(line)["index"]


def MergeAll(folder):
    terms = sorted(getAllUniqueTerms(folder))
    print(len(terms))
    # indexDict = {1: }
    for key in terms:
        mydict = findAllValues(folder, key)
        with open("finalIndex/MergedIndex.jsonl", "a") as d:
            json.dump(mydict, d)
            d.write("\n")
            d.write("\n")
            print("im done!")
            mydict = {}

        # mydict = {} # clear dictionary
        # createIndexOfIndexes(json_file, "finalIndex/IndexOfIndexes.json")


def mergeDict(folder):
    count = 0
    for json_file in folder.rglob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)
            dict = {}
            for key,value in data.items():
                dict[key] = value
            with open("finalIndex/MergedDictIndex.jsonl", "a") as d:
                json.dump(dict, d)
                d.write ("\n")
        print("finished")
    with open("finalIndex/MergedDictIndex.jsonl", "r") as d:
        data = {}
        for line in d:
            entry = json.loads(line)  # Load each line as a separate JSON object
            data.update(entry)  # Merge each dictionary into one

        print(len(list(data.keys())))

def getLines():
    with open(indexDict[0] ,"r") as w:
        count = sum(1 for _ in w)
    return count