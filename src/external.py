import json
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

if __name__ == "__main__":
    convertToTxt()
    createIndexOfIndexesTxt()

