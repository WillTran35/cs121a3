import re
from nltk.stem import PorterStemmer
import json
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from Document import Document

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

def tokenize(file_path:str) -> list:
    # This function runs in O(n) time complexity because it takes each line and passes into tokenizeline() which runs in
    # O(n) complexity
    result = []
    with open(file_path, "r") as line:
        for i in line:
            result += tokenizeline(i)
    return result

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

    # with open("../results.json", "r") as f:
    #     results: dict = json.load(f)
    words = {}
    pages = {}
    partial_index = {}
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
            for i in stemmed_tokens:
                if i not in newDoc.getTokensAndFreq():
                    newDoc.getTokensAndFreq()[i] = newDoc.getTokensAndFreq().get(i,0) + 1

                # if url not in pages:
                #     pages[url] = {}
                #     pages[url][i] = 1
                # else:
                #     pages[url][i] = pages[url].get(i, 0) + 1
                # print(pages)
                # print(words)
            count += 1
            partial_index[newDoc.getID()] = newDoc
    for i in words:
        words[i] = list(words[i])
    print(count)

    try:
        with open("../results.json", "w") as f:
            json.dump(words, f, indent =4)
        with open("../pages.json", "w") as f:
            json.dump(pages, f, indent=4)
    except Exception as e:
        print(e)
        # print(words)



if __name__ == "__main__":
    run()
    with open("../results.json", "r") as f:
        data = json.load(f)
        keys = list(data.keys())
        # print(keys)
        print(len(keys))  # 387,833 , 1,066,672

    with open("../pages.json") as f:
        data = json.load(f)
        keys = list(data.keys())
        # print(keys)
        print(len(keys))  # 54,879 # 55,086
    # pd.