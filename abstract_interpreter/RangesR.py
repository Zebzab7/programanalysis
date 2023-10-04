class Ranges_abstract():
    def __init__(self,start,end):
        self.start = start
        self.end = end
    def toString(self):
        return "start:" + str(self.start) + " end:" + str(self.end)
    def __eq__(self, other):
        if (self.start == other.start and self.end == other.end):
            return True
        return False            