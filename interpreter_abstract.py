from pathlib import Path
from logging import log

import json
from interpretertest import *

class Interpreter:
    def __init__(self):
        self.classes = {}
        self.memory = {}

    def get_json(self, json_file):
        with open(json_file) as f:
            data = json.load(f)
        return data
    
    #Get all class names 
    def get_class(self, data):
        self.classes[data["name"]] = data
        self.classes = self.classes
    
    # Get methods in classes for a particular class
    def get_methods(self):
        methods = {}
        for clas in self.classes.values():
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
        if absolute_method[0] not in self.classes:
            return absolute_method[1]
        methods = self.classes[absolute_method[0]]["methods"]
        for method in methods:
            print("method name: ", method["name"])
            if method["name"] == absolute_method[1]:
                return method
    
    def ifstack(self, boolean, target,pc):
        if boolean:
            return target-1 #Get's the one before and then incremented
        return pc
    
    def incrementPc(self,local_stack):
        absolute_method = local_stack[2][0]
        return (local_stack[0], local_stack[1], (absolute_method, local_stack[2][1] + 1))

    def get_from_bytecode(self, bytecode, local_stack):
        result = None

        get_field = bytecode["field"]
        if "type" in get_field:
            local_stack[1].append(get_field["type"]["name"] + get_field["name"])
        else:
            local_stack[1].append(get_field["name"])
        return result

    def interpret(self, absolute_method, pc, log, memory, args):
        print("Absolute method: ", absolute_method)
        # λ,σ,ι
        local_stack = ([],[],(absolute_method, pc))
        method = self.find_method(absolute_method)
        if method == absolute_method[1]:
            log("executing method: ", absolute_method[1], " with arguments: ", args)
            # return None,None

        # Load in arguments
        for arg in args:
            local_stack[0].append(arg)

        bytecode_statements = method["code"]["bytecode"]
        length = len(bytecode_statements)
        while local_stack[2][1]<length: #(i,seq[0])
            pc = local_stack[2][1] #PC
            bytecode = bytecode_statements[pc]
            print(bytecode)
            if bytecode["opr"] == "return":
                if bytecode["type"] == None:
                    log("(return) None")
                    return None,None
                elif bytecode["type"] == "int":
                    log("(return) int: ", local_stack[1][-1])
                    return local_stack[1][-1] #Returns the last element in the opr. stack
                else:
                    log("return type not implemented "+ bytecode["type"])
                log(local_stack)
            elif bytecode["opr"] == "push":
                log("(push)")
                local_stack[1].append((bytecode["value"]["type"], bytecode["value"]["value"]))
                log(local_stack)
            elif bytecode["opr"] == "load":  
                log("(load)")
                lv_type, value = local_stack[0][bytecode["index"]]
                local_stack[1].append((lv_type, value))
                log(local_stack)
            elif bytecode["opr"] == "binary": 
                if bytecode["operant"] == 'add':
                    log("(add)")
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var1 + var2))
                    log(local_stack)
                elif bytecode["operant"] == 'mul':
                    log("(mul)")
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var1 * var2))
                    log(local_stack)
                elif bytecode["operant"] == 'sub':
                    log("(sub)")
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var2 - var1))
                    log(local_stack)
                else:
                    print("operant not supported " + bytecode["operant"])
            elif bytecode["opr"] == "store":
                log("(store)")
                lv_type, val = local_stack[1].pop()
                
                if bytecode["index"] < len(local_stack[0]):
                    local_stack[0][bytecode["index"]] = (lv_type, val)
                else: 
                    local_stack[0].append((lv_type, val))
                log(local_stack)
                
            elif bytecode["opr"] == "incr":   
                log("(incr)")
                lv_type, value = local_stack[0][bytecode["index"]]
                local_stack[0][bytecode["index"]] = (lv_type, value + bytecode["amount"])
                log(local_stack)
            elif bytecode["opr"] == "goto": 
                log("(goto)")
                local_stack = (local_stack[0], local_stack[1], (absolute_method, bytecode["target"]-1))
                log(local_stack)
            elif bytecode["opr"] == "if": #Collin
                log("(if)")
                log(bytecode["condition"])
                left,left_val = local_stack[1][-2]
                right,right_val = local_stack[1][-1]
                if bytecode["condition"] == "gt":
                    gt = left_val > right_val
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(gt, bytecode["target"],pc)))
                    log(local_stack)
                elif bytecode["condition"] == "lt":
                    lt = left_val < right_val
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(lt, bytecode["target"],pc)))
                    log(local_stack)
                elif bytecode["condition"] == "eq":
                    eq = left_val == right_val
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(eq, bytecode["target"],pc)))  
                    log(local_stack)
                elif bytecode["condition"] == "ge":
                    ge = left_val >= right_val
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(ge, bytecode["target"],pc)))  
                    log(local_stack)
                else:
                    print("if type not implemented" + str(bytecode["condition"]))
                local_stack[1].pop()
                local_stack[1].pop()
            elif bytecode["opr"] == 'ifz': #if zero
                log("(ifz)")
                lv_type,val = local_stack[1][-1]
                if bytecode["condition"] == "lz":
                    lz = (val == 0)
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(lz, bytecode["target"],pc)))
                    log(local_stack)
                elif bytecode["condition"] == "le":
                    le = (val <= 0)
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(le, bytecode["target"],pc)))
                    log(local_stack)
                else:
                    print("ifz type not implemented" + str(bytecode["condition"]))
                local_stack[1].pop()
            elif bytecode["opr"] == "get":
                log("(get)")
                if 'Array' in str(bytecode["field"]["class"]):
                    memory["array"].append(bytecode)
                    log(memory)
                elif 'class' in bytecode["field"]["class"]:
                    cn = bytecode["field"]["type"]["name"]
                    fs = None
                    memory["class"].append((cn, fs))
                    log(memory)
                else:
                    print("get type not implemented" + str(bytecode["field"]))
            elif bytecode["opr"] == "invoke":
                log("(invoke)")
                if bytecode["access"] == "virtual" or bytecode["access"] == "static":
                    args_type = bytecode["method"]["args"] #Kind, Name 
                    args = []
                    for args_type in args_type:
                        args.append(local_stack[1].pop())
                    args.reverse()
                    am = (bytecode["method"]["ref"]["name"], bytecode["method"]["name"])
                    
                    # absolute_method, pc, log, memory, args
                    returned_element = self.interpret(am, 0, print, memory, args)
                    if returned_element != None:
                        local_stack[1].append(returned_element)
                        log(local_stack)
                # elif bytecode["access"]=="dynamic":
                #     if bytecode["method"]["args"] is not None:  
                elif bytecode["access"] == "special":
                    if bytecode["method"]["name"] == "<init>":
                        local_stack[1].append(bytecode["method"]["name"])
                        log(local_stack)
                else:
                    print("Invoke type not supported" + bytecode["access"])
            else:
                print("bytecode opr not implemented" + str(bytecode["opr"]))
                
                log(local_stack)
            local_stack=self.incrementPc(local_stack)
        return None

def traverse_files():
    path = Path("bin/course-examples/json")
    files = []
    for f in path.glob("**/*.json"):
        files.append(f)
    return files

def tests(interpreter):
    runConcrete(interpreter)
    print("all tests fine :D")
    return

def main():
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    files = traverse_files()
    interpreter = Interpreter()
    for f in files:
        data = interpreter.get_json(f)
        interpreter.get_class(data)
    # tests(interpreter)

main()