from pathlib import Path
import json
from util import *

class Interpreter:
    def __init__(self, memory, methods):
        self.memory = memory
        self.methods = methods
    def find_method(self,fileName,methodName):
        for file in self.methods:
            if file.getName() == fileName:
               for method in file.getMethods():
                    print(method)
                    if method == methodName:
                        return file.getMethods()[method]
        assert False, "NO METHOD FOUND"

    def interpret(self,file, methodName,pc, log, mem,args):
        if args == "":
            args = "No args"
        print("Interpreting method: " + methodName + " with arguments: " + args) 
        int_constants = []
        local_vars = []
        method = self.find_method(file,methodName)
        print(method)
        # λ,σ,ι
        local_stack = (local_vars,[],(methodName,pc))
        


        

def traverse_files(pathtext):
    files = []
    path = Path(pathtext)
    for file in path.glob('**/*.json'):
        files.append(file)
    return files

def get_json(file):
    with open(file) as f:
        data = json.load(f)
        #json file name
        name = data['name'].split('/')[-1]
        methods = {}
        for method in data["methods"]:
            methods[method['name']] = method
        file = fileholder(name,methods)
    return file


def main():
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    files = traverse_files('bin')
    jfiles = []

    for f in files:
        jfiles.append(get_json(f))
    for jfile in jfiles:
        print(jfile.getName())
        print(jfile.getMethods().keys())
    interpreter = Interpreter(memory,jfiles)
    interpreter.interpret("Simple","noop",0,print,memory,"")

    
main()