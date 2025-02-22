class Document:
    def __init__ (self, ID, url, tokens, encoding):
        self.ID = "Doc" + ID
        self.url = url
        self.tokens = tokens
        self.encoding = encoding

    def getID(self):
        return self.ID

    def getUrl(self):
        return self.url

    def getTokensAndFreq(self):
        return self.tokens

    def getEncoding(self):
        return self.encoding