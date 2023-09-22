from pathlib import Path
import json

class Interpreter:
    def __init__(self, json_file):
        self.json_file = json_file
        self.classes = None

    def get_json(self):
        with open(self.json_file) as f:
            data = json.load(f)
        return data
    
    #Get all class names 
    def get_classes(self, data):
        classes = {}
        classes[data["name"]] = data
        self.classes = classes
        return classes
    
    # Get methods in classes for a particular class
    def get_methods(self, classes):
        methods = {}
        for clas in classes.values():
            for method in clas["methods"]:
                methods[method["name"]] = method
        return methods
    
    #Get all annotations in methods for a particular method
    def get_annotations(self, methods):
        annotations = {}
        for method in methods.values():
            for annotation in method["annotations"]:
                annotations[annotation["type"]] = annotation
        return annotations
    
    def get_classes_methods(self, classes, methods):
        classes_methods = set()
        for clas in classes.values():
            for method in clas["methods"]:
                classes_methods.add((clas["name"], method["name"]))
        return classes_methods
    
    def get_bytecode(self, methods):
        bytecode = {}
        for method in methods.values():
            for annotation in method["annotations"]:
                    if annotation["type"] == "dtu/compute/exec/Case":
                        bytecode[method["name"]] = method["code"]["bytecode"]
        return bytecode
    
    def find_method(self, absolute_method):
        methods = self.classes[absolute_method[0]]["methods"]
        for method in methods:
            if method["name"] == absolute_method[1]:
                return method

    def interpret(self, absolute_method, log):
        memory = {}
        stack = [([],[],(absolute_method, 0))]
        method = self.find_method(absolute_method)
        bytecodes = method["code"]["bytecode"]
        for i in range(len(bytecodes)):
            (lv, os, (absolute_method_,pc)) = stack[-1]
            bytecode = bytecodes[i]
            if bytecode["opr"] == "return":
                if bytecode["type"] == None:
                    log("(return)")
                    return None
       

def traverse_files():
    path = Path("bin/course-examples/json")
    files = []
    for f in path.glob("**/Simple.json"):
        files.append(f)
    return files
    
def main():
    files = traverse_files()
    for f in files:
        interpreter = Interpreter(f)
        data = interpreter.get_json()
        classes = interpreter.get_classes(data)
        methods = interpreter.get_methods(classes)
        annotations = interpreter.get_annotations(methods)
        cases = [("dtu/compute/exec/Simple", "noop")]
        for case in cases:
            statement = interpreter.interpret(case, print)
            print(statement)
        classes_methods = interpreter.get_classes_methods(classes, methods)

main()