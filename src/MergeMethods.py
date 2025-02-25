import json
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


