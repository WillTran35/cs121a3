import json
from pathlib import Path
from constants import sortByFreq
def splitIndex():
    """Opens the final index and splits the index into separate lists based off of first char."""
    with open("finalIndex/final_IndexFINAL.jsonl", "r") as r:
        string = ""
        letters = []
        while True:
            line = r.readline()
            if not line:
                break
            obj = json.loads(line)
            term = obj["term"]
            index = obj["index"]
            idf = obj["idf_score"]
            if len(letters) == 0:
                string += f"{term}|{index}|{idf}\n"
                letters.append(term[0])
                print(letters)
            elif term[0] in letters:
                string += f"{term}|{index}|{idf}\n"
            else:
#                 dump to file, clear string
                print(letters)
                with open(f"Indexes/{letters[-1]}_index.txt", "w") as w:
                    w.write(string)
                    print(f"wrote {letters[-1]}")
                    letters.append(term[0])
                    string = f"{term}|{index}|{idf}\n"
        if string:
            with open(f"Indexes/{term[0]}_index.txt", "w") as w:
                w.write(string)
                print(f"wrote {letters[-1]}")
                letters.append(term[0])

def countLines():
    folder = Path("Indexes/")
    count = {}
    for file in folder.rglob("*.txt"):
        with open(file,"r") as r:
            length = 0
            while True:
                line = r.readline()
                if not line:
                    break
                length += 1
            count[file.name] = length
    return sortByFreq(count)

def createSkipList():
    folder = Path("Indexes/")

    for file in folder.rglob("*.txt"):
        with open(file, "r") as r:
            count = 1
            num_lines = countLines()[file.name]
            print(num_lines)
            string = ""
            while True:
                line = r.readline()
                position = r.tell()
                if not line:
                    break
                word = line[0:line.find("|")]
                # print(word)
                if count % 250 == 0 or count == 1:
                    string += f"{word}|{position}\n"
                elif count == num_lines:
                    string += f"{word}|{position}\n"
                    print(f"im here {count}")
                count += 1
            with open(f"SkipLists/{file.name[0]}_skiplist.txt", "w") as w:
                w.write(string)


def run():
    splitIndex()
    createSkipList()


if __name__ == "__main__":
    run()
