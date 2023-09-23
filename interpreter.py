from pathlib import Path
from logging import log
import json

class Interpreter:
    def __init__(self, json_file):
        self.json_file = json_file
        self.classes = None
        self.memory = {}

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
    
    def find_method(self, absolute_method):
        methods = self.classes[absolute_method[0]]["methods"]
        for method in methods:
            if method["name"] == absolute_method[1]:
                return method
    
    def ifstack(self, boolean, target):
        if boolean:
            return 1
        return target

    def interpret(self, absolute_method, pc,log):
        print("Absolute method: ", absolute_method)
        
        # λ,σ,ι
        local_stack = ([None, None],[],(absolute_method, pc))
        # stack_list = [([],[],(absolute_method, pc))] 
        method = self.find_method(absolute_method)
        bytecode_statements = method["code"]["bytecode"]
        length = len(bytecode_statements)

        # TODO Read parameters of function and put them in the stack 

        while local_stack[2][1]<length: #(i,seq[0])

            bytecode = bytecode_statements[local_stack[2][1]]
            if bytecode["opr"] == "return":
                if bytecode["type"] == None:
                    log("(return) None")
                    return None
                elif bytecode["type"] == "int":
                    return local_stack[0][-1] #Returns the last element in the stack
                else:
                    log("return "+ bytecode["type"])
            elif bytecode["opr"] == "push":
                log("(push)")
                local_stack[1].append(bytecode["value"])
                local_stack = (local_stack[0], local_stack[1], (absolute_method, local_stack[2][1] + 1))
                log(local_stack)
            elif bytecode["opr"] == "load":   #Shreyas
                log("(load)")
                local_stack[0][bytecode["index"]] = bytecode["type"]
                local_stack = (local_stack[0], local_stack[1], (absolute_method, local_stack[2][1] + 1))
                log(local_stack)
            elif bytecode["opr"] == "binary":    #Shreyas
                if bytecode["operant"] == 'add':
                    pass
                    # log("(add)")
                    # local_stack.append((local_stack[-2][0], local_stack[-1])[1] + local_stack[-2][1])
                elif bytecode["operant"] == 'mul':
                    pass
            elif bytecode["opr"] == "store":
                log("(store)")
                var = local_stack[1].pop(-1)
                local_stack[0][bytecode["index"]] = var
                pass
            elif bytecode["opr"] == "incr":   #Shreyas
                pass
            elif bytecode["opr"] == "goto": 
                log("(goto)")
                local_stack = (local_stack[0], local_stack[1], (absolute_method, bytecode["target"]))
                pass
            elif bytecode["opr"] == "if": #Collin
                log("(if)")
                if bytecode["condition"] == "gt":
                    gt = local_stack[-2][1] > local_stack[-1][1]
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(gt, bytecode["target"])))
                if bytecode["condition"] == "lt":
                    lt = local_stack[-2][1] < local_stack[-1][1]
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(lt, bytecode["target"])))
                if bytecode["condition"] == "eq":
                    eq = local_stack[-2][1] == local_stack[-1][1]
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(eq, bytecode["target"])))  
                else:
                    print("if type not implemented" + str(bytecode["condition"]))
                pass
            elif bytecode["opr"] == "get":
                pass
            elif bytecode["opr"] == 'ifz': #if zero
                if bytecode["condition"] == "lz":
                    lz = local_stack[-1][1] == 0
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(lz, bytecode["target"])))
                else:
                    print("ifz type not implemented" + str(bytecode["condition"]))
                pass
            elif bytecode["opr"] == "invoke":
                pass
            elif bytecode["opr"] == "binary":
                pass
            else:
                print("bytecode opr not implemented" + str(bytecode["opr"]))
                local_stack = (local_stack[0], local_stack[1], (absolute_method, local_stack[2][1] + 1))

        return local_stack

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
        cases = [("dtu/compute/exec/Simple", "noop"), ("dtu/compute/exec/Simple", "zero"), 
                 ("dtu/compute/exec/Simple", "hundredAndTwo"), ("dtu/compute/exec/Simple", "identity"),
                 ("dtu/compute/exec/Simple", "add")]
        for case in cases:
            stack = interpreter.interpret(case, 0,print)
            
            #print(stack)
            #print()
        classes_methods = interpreter.get_classes_methods(classes, methods)
main()

