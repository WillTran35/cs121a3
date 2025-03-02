class Task:
    def __init__(self, term, index, location, position):
        self.term = term
        self.index = index
        self.location = location
        self.position = position

    def __lt__(self, other):
        return self.term < other.term

    def getTerm(self):
        return self.term

    def getIndex(self):
        return self.index

    def getLocation(self):
        return self.location

    def getPosition(self):
        return self.position

    def __repr__(self):
        return f'({self.term}, {self.position})'
