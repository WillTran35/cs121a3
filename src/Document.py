class Document:
    def __init__ (self, ID, url, tokens, encoding):
        self.ID = "Doc" + str(ID)
        self.url = url
        self.tokens = tokens
        self.encoding = encoding

    def __repr__(self):
        return self.ID

    def getID(self):
        return self.ID

    def getUrl(self):
        return self.url

    def getTokensAndFreq(self):
        return self.tokens

    def getEncoding(self):
        return self.encoding

    def isInTokensAndFreq(self, token):
        return token in self.getTokensAndFreq()

    def getFrequencyOfToken(self, token):
        if self.isInTokensAndFreq(token):
            return self.getTokensAndFreq()[token]
