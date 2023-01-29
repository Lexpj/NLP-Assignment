"""
BLACKLIST class to filter out used rhymewords when continuing the rhyme
"""
class Blacklist():
    def __init__(self):
        self.blacklist = []
    def filter(self,a):
        return [x for x in a if x not in self.blacklist]
    def clear(self):
        self.blacklist = []
    def add(self,a):
        self.blacklist.append(a)