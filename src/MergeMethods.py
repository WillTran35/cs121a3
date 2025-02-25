import json
import re

pattern = r'Doc\d+'

def createNewPartialJson(count, partial_index):
    with open(f"jsonFolder/{count - 10000}-{count}.json", "w") as f:
        data = {}
        for key, item in partial_index.items():
            if key in data:
                data[key].update({x.getID(): x.getFrequencyOfToken(key) for x in item})
            else:
                data[key] = {x.getID(): x.getFrequencyOfToken(key) for x in item}
        json.dump(data, f, indent=1)

def createNewDictPartialJson(count, dictList):
    with open(f"DictJsonFolder/{count - 10000}-{count}.json", "w") as f:
        data = {}
        for key, item in dictList.items():
            data[key] = item
        json.dump(data, f, indent=1)

def createIndexOfIndexes(json_index_file, index_of_index_file):
    indexOfIndex = {}
    pass


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
    for json_file in folder.rglob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)
            for key in data.keys():
                terms.add(key)
    return terms


def MergeAll(folder):
    count = 0
    terms = getAllUniqueTerms(folder)
    print(len(terms))
    for key in terms:
        mydict = findAllValues(folder, key)
        with open("finalIndex/MergedIndex.jsonl", "a") as d:
            json.dump(mydict, d)
            count += 1
            print(count)
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
