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
    
    def get_bytecodes(self, methods):
        bytecode = {}
        for method in methods.values():
            for annotation in method["annotations"]:
                    if annotation["type"] == "dtu/compute/exec/Case":
                        bytecode[method["name"]] = method["code"]["bytecode"]
        return bytecode
    
    def get_bytecode(self, absolute_method, methods):
        #absolute_method: (class name, method name)
        name = absolute_method[1]
        for method in methods:
            if method["name"] == name:
                return method["code"]["bytecode"]
    
    def find_method(self, absolute_method):
        methods = self.classes[absolute_method[0]]["methods"]
        for method in methods:
            if method["name"] == absolute_method[1]:
                return method
    
    def interpret_function(self, absolute_method):
        bytecode = self.get_bytecode(self, absolute_method)
        return
        # (lv, os, (absolute_method_,pc)) = stack[-1]
        # for i, v in enumerate(bytecode):
        #     (l, s, (am1,i)) = methods_stack[-1]
        #     # the operation that index of i
        #     # different operation {load,return,push,binary,if,goto,store,incr...}
        #     # basic key in bytecode {offset,opr,type}
        #     if v["opr"] == "return":
        #         if v["type"] == "null":
        #             log("return")
        #         else:
        #             log("return "+ v["type"])
        #     elif v["opr"] == "push":
        #         log("push")
        #         methods_stack.append(l,s.append(v["value"]),(am,i+1))
        #     elif v["opr"] == "load":
        #         log("load parameter"+ v["type"])
        #     elif "target" in v:
        #         l[v["target"]]

    # bytecode_info("offset","opr","type")
    def interpret_bytecodes(self, methods):
        absolute_method = self.find_method(self, ("dtu/compute/exec/Simple", "noop"))
        
        memory = {}
        stack = [([],[],(absolute_method, 0))]

        #{"name": bytecodes}
        bytecodes = self.get_bytecodes(self, methods)
        
        for name, bytecode in bytecodes:
            for opr in bytecodes[name]:
                self.interpret(self, absolute_method)
        return
        
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