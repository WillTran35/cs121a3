import re
from nltk.stem import PorterStemmer


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
    """Write a method/function that reads in a text file and returns a list of the tokens
    in that file. For the purposes of this project, a token is a sequence of alphanumeric characters,
    independent of capitalization (so Apple, apple, aPpLe are the same token).
    You are allowed to use regular expressions if you wish to (and you can use some regexp engine,
    no need to write it from scratch), but you are not allowed to import a tokenizer (e.g. from NLTK),
    since you are being asked to write a tokenizer."""

    # This function runs in O(n) time complexity because it takes each line and passes into tokenizeline() which runs in
    # O(n) complexity
    result = []
    with open(file_path, "r") as line:
        for i in line:
            result += tokenizeline(i)
    return result

def run():
    pass


if __name__ == "__main__":
    pass
