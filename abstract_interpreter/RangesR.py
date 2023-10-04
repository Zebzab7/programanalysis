class Ranges_abstract():
    def __init__(self,start,end):
        self.start = start
        self.end = end
    def __str__(self):
        return "start:" + str(self.start) + " end:" + str(self.end)
    def __repr__(self):
        return "Range: {" + str(self.start) + ", " + str(self.end) + "}"
    def toString(self):
        return "start:" + str(self.start) + " end:" + str(self.end)
    def __eq__(self, other):
        # First check the type of the other object
        if (type(self) != type(other)):
            return False
        if (self.start == other.start and self.end == other.end):
            return True
        return False            