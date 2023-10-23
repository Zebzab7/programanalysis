class fileholder:
    def __init__(self,name,methods):
        self.name = name
        self.methods = methods
    def __str__(self):
        return self.name + str(self.methods.keys())
    def getName(self):
        return self.name
    def getjsonfile(self):
        return self.jsonfile
    def getMethods(self):
        return self.methods

