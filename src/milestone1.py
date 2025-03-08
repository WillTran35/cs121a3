from nltk.stem import PorterStemmer
import json
from pathlib import Path
from bs4 import BeautifulSoup
from Document import Document
from Final_Index import Final_Index
import MergeMethods
import searchMethods
import time
from constants import tokenizeline, indexDict, DictIndex

def dumpToFinalIndex(words: dict):
    try:
        with open("../results.json", "w") as f:
            json.dump(words, f, indent=4)
    except Exception as e :
        print(e)

def parseHTML(html: str, encoding):
    soup = BeautifulSoup(html, "html.parser", from_encoding=encoding)

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
            html_string = parseHTML(html, encoding)
            length_of_doc = len(html_string)
            stemmed_tokens = [stemmer.stem(i) for i in tokenizeline(html_string)]

            newDoc = Document(count, url, {}, encoding)
            idsToDict[newDoc.getID()] = newDoc.getUrl()
            for i in stemmed_tokens:
                newDoc.getTokensAndFreq()[i] = newDoc.getTokensAndFreq().get(i, 0) + 1  # document dict has token
                # as key and frequency as value


            for i in newDoc.getTokensAndFreq().keys():
                newDoc.getTokensAndFreq()[i] = newDoc.getFrequencyOfToken(i) / length_of_doc  # tf score
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

def restartIndex():
    run()
    MergeMethods.createIndexOfIndexes(Path("jsonFolder/"))
    MergeMethods.prioQ()
    MergeMethods.mergeDict()
    MergeMethods.createFinalIndexOfIndexes()

if __name__ == "__main__":
    start = time.time()
    # restartIndex()
    x = searchMethods.querySearch("master of software engineering")
    # x = searchMethods.getPosition("softwar", 7)
    # print(x)
    end = time.time()
    print(end-start)
    # MergeMethods.createFinalIndexOfIndexes()


