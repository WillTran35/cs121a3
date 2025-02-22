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
        with shelve.open("final_index") as index:
            if self.name not in index:
                index[self.name] = []
            temp = []
            temp.append(objList)
            index[self.name] = temp
