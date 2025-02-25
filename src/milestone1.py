import re
from nltk.stem import PorterStemmer
import json
from pathlib import Path
from bs4 import BeautifulSoup
from Document import Document
from Final_Index import Final_Index
import MergeMethods


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

def dumpToFinalIndex(words: dict):
    try:
        with open("../results.json", "w") as f:
            json.dump(words, f, indent=4)
    except Exception as e :
        print(e)

def parseHTML(html: str):
    soup = BeautifulSoup(html, "html.parser" )

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return text

def run():
    # for each document parse the json file
    # get the html tag and parse the file
    # tokenize the file and put all in a list
    # stem all the words
    # add to dictionary
    # json file just has url, HTML, and encoding

    dev_folder = Path("/Users/willtran/Downloads/DEV")


    stemmer = PorterStemmer()

    words = {}
    pages = {}
    partial_index = {}  # token is the key: (Document, frequency)
    final_index = Final_Index()
    idsToDict = {}
    count = 0
    for json_file in dev_folder.rglob("*.json"):
        with json_file.open("r") as file:
            data = json.load(file)
            url = data['url']
            html = data['content']
            encoding = data['encoding']
            print(url)
            html_string = parseHTML(html)
            stemmed_tokens = [stemmer.stem(i) for i in tokenizeline(html_string)]

            newDoc = Document(count, url, {}, encoding)
            idsToDict[newDoc.getID()] = newDoc.getUrl()
            for i in stemmed_tokens:
                newDoc.getTokensAndFreq()[i] = newDoc.getTokensAndFreq().get(i, 0) + 1  # document dict has token
                # as key and frequency as value
            for i in newDoc.getTokensAndFreq().keys():
                if i not in partial_index:
                    partial_index[i] = [newDoc]
                else:
                    partial_index[i].append(newDoc)

        count += 1
        if count % 10000 == 0:
            MergeMethods.createNewPartialJson(count, partial_index)
            # final_index.update_doc_dict(idsToDict, flag=1)
            MergeMethods.createNewDictPartialJson(count, idsToDict)
            partial_index = {}
            idsToDict = {}

    # final_index.dump_to_disk_not_empty(partial_index)
    if partial_index:
        MergeMethods.createNewPartialJson(count, partial_index)
        MergeMethods.createNewDictPartialJson(count,idsToDict)
    partial_index = {}
    idsToDict = {}


if __name__ == "__main__":
    # run()
    print(len(MergeMethods.getAllUniqueTerms(Path("jsonFolder/"))))
    # MergeMethods.sortJsonLkeys(Path("jsonFolder/"))
    # MergeMethods.MergeAll(Path("jsonFolder/"))
    # MergeMethods.mergeDict(Path("DictJsonFolder/"))
    # with open("../results.json", "r") as f:
    #     data = json.load(f)
    #     keys = list(data.keys())
    #     # print(keys)
    #     print(len(keys))  # 387,833 , 1,066,672
    #
    # with open("../pages.json") as f:
    #     data = json.load(f)
    #     keys = list(data.keys())
    #     # print(keys)
    #     print(len(keys))  # 54,879 # 55,086
    # pd.
    # with shelve.open("final_index2") as a:
    #     # a["hi"] = Document(9, "j", {}, "i")
    #     print(a["hi"])