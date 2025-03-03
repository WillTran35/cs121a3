import re

indexDict = {0: "jsonFolder/0-10000.jsonl", 1: "jsonFolder/10000-20000.jsonl",
             2: "jsonFolder/20000-30000.jsonl", 3: "jsonFolder/30000-40000.jsonl",
             4: "jsonFolder/40000-50000.jsonl", 5: "jsonFolder/45393-55393.jsonl",
             6: "finalIndex/final_IndexFINAL.jsonl", 7: "IndexOfIndexes/final-IndexOfIndexes.jsonl"}

lengthIndexDict = {0: 37093, 1: 96755, 2: 131919, 3: 133182, 4: 752206,
                   5: 449101, 6: 1066672, 7: 1066672 }

countDict = {"jsonFolder/0-10000.jsonl": 0, "jsonFolder/10000-20000.jsonl": 1,
            "jsonFolder/20000-30000.jsonl": 2, "jsonFolder/30000-40000.jsonl": 3,
             "jsonFolder/40000-50000.jsonl": 4, "jsonFolder/45393-55393.jsonl": 5}

indexOfIndexDict = {"IndexOfIndexes/0-IndexOfIndexes.jsonl": 0, "IndexOfIndexes/1-IndexOfIndexes.jsonl": 1,
                    "IndexOfIndexes/2-IndexOfIndexes.jsonl": 2, "IndexOfIndexes/3-IndexOfIndexes.jsonl": 3,
                    "IndexOfIndexes/4-IndexOfIndexes.jsonl": 4, "IndexOfIndexes/5-IndexOfIndexes.jsonl": 5}


def tokenizeline(line:str) -> list:
    """Helper function to tokenize an individual line."""
    # This function runs in O(n) time complexity, where n is the length of the line.
    # It must iterate through the entire string getting each letter.
    result = []
    string = ""
    line = line.lower()
    pattern = "^[a-zA-Z0-9]"
    for i in line:
        if re.search(pattern, i):
            string += i
        else:
            if string != "":
                result.append(string)
            string = ""
    if string != "":
        result.append(string)
    return result


