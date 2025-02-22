import shelve

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


    def dump_to_disk(self, objList):
        with shelve.open("final_index",  flag="c", protocol=4) as index:
            for i, j in objList.items():
                print(i, j)
                index[i] = j
                print("done")
            # print(list(index.keys()))