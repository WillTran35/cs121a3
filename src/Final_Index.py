import shelve
import json
import os

class Final_Index:
    def __init__(self):
        self.name = "main"

    def getNumTokens(self):
        with shelve.open("final_index") as index:
            tokens = set()
            if self.name not in index:
                return 0
            for i in index[self.name]:
                for j in i.keys():
                    tokens.add(j) # need to work on this

    def printIndex(self):
        with shelve.open("final_index") as index:
            print(index[self.name])

    def addToData(self, data, objList):
        for key, item in objList.items():
            if key in data:
                data[key].update({x.getID(): x.getFrequencyOfToken(key) for x in item})
            else :
                data[key] = {x.getID(): x.getFrequencyOfToken(key) for x in item}
        return data

    def dump_to_disk(self, objList):
        # with shelve.open("final_index",  flag="c", protocol=4) as index:
        #     for i, j in objList.items():
        #         print(i, j)
        #         index[i] = [x.getID() for x in j]
        #         print("Yo")
        #         print(i, index[i])
            # print(list(index.keys()))
            # for i, j in index.items():
            #     print(i,j)
        # with open("../results2.json", "r") as f:
        #     data = json.load(f)
        data = {}
        data = self.addToData(data,objList)
        with open("../results2.json", "w") as f:
            json.dump(data, f, indent=1)

    def dump_to_disk_not_empty(self,objList):
        with open("../results2.json", "r") as f:
            data = json.load(f)
        data = self.addToData(data, objList)
        with open("../results2.json", "w") as f:
            json.dump(data, f, indent=4)
            # data = json.load(f)
            # keys = list(data.keys())
            # # print(keys)
            # print(len(keys))  # 387,833 , 1,066,672

    def updateDictData(self, data, dictList):
        for key, item in dictList.items():
            data[key] = item

        with open("../dictList.json", "w") as f:
            json.dump(data, f, indent=4)

    def update_doc_dict(self, dictList, flag):
        if flag == 1:
            #  empty json
            data = {}
        else:
            with open("../dictList.json", "r") as f:
                data = json.load(f)
        self.updateDictData(data, dictList)

    def getNumTokens(self):
        with open("../results2.json", "r") as f:
            data = json.load(f)
            return len(list(data.keys()))


    def getNumDocuments(self):
        with open("../dictList.json", "r") as f:
            data = json.load(f)
            return len(list(data.keys()))

if __name__ == "__main__":
    with open("../results2.json", "r") as f:
        data = json.load(f)
        print("Tokens: " + str(len(list(data.keys()))))
        # print(len(data["class"]))
        print("Size: " + str(os.path.getsize("../results2.json")))  #  306,840.63 KB, 299.26 MB

    with open("../dictList.json", "r") as f:
        data = json.load(f)
        print("Unique Documents: " + str(len(list(data.keys()))))

