from pathlib import Path
from logging import log
import random
import json
import sys
import math
import sympy

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
        if absolute_method[0] not in self.classes:
            return absolute_method[1]
        methods = self.classes[absolute_method[0]]["methods"]
        for method in methods:
            if method["name"] == absolute_method[1]:
                return method
    
    def ifstack(self, boolean, target,pc):
        if boolean:
            return target
        return pc+1
    
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
        local_stack = self.incrementPc(local_stack)

        return result

    def interpret(self, absolute_method, pc, log, memory, args):
        print("Absolute method: ", absolute_method)
        
        # λ,σ,ι
        local_stack = ([],[],(absolute_method, pc))
        method = self.find_method(absolute_method)
        if method == absolute_method[1]:
            log("executing method: ", absolute_method[1], " with arguments: ", args)
            return None

        # Load in arguments
        for arg in args:
            local_stack[0].append(arg)

        bytecode_statements = method["code"]["bytecode"]
        length = len(bytecode_statements)
        while local_stack[2][1]<length: #(i,seq[0])
            pc = local_stack[2][1] #PC
            bytecode = bytecode_statements[pc]
            if bytecode["opr"] == "return":
                if bytecode["type"] == None:
                    log("(return) None")
                    return None
                elif bytecode["type"] == "int":
                    return local_stack[1][-1] #Returns the last element in the opr. stack
                else:
                    log("return type not implemented "+ bytecode["type"])
            elif bytecode["opr"] == "push":
                log("(push)")
                local_stack[1].append((bytecode["value"]["type"], bytecode["value"]["value"]))
                local_stack = self.incrementPc(local_stack)
                log(local_stack)
            elif bytecode["opr"] == "load":  
                log("(load)")
                lv_type, value = local_stack[0][bytecode["index"]]
                local_stack[1].append((lv_type, value))
                local_stack = self.incrementPc(local_stack)
                log(local_stack)
            elif bytecode["opr"] == "binary": 
                if bytecode["operant"] == 'add':
                    log("(add)")
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var1 + var2))
                    local_stack = self.incrementPc(local_stack)
                    log(local_stack)
                elif bytecode["operant"] == 'mul':
                    log("(mul)")
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var1 * var2))
                    local_stack = self.incrementPc(local_stack)
                    log(local_stack)
                elif bytecode["operant"] == 'sub':
                    log("(sub)")
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var1 - var2))
                    local_stack = self.incrementPc(local_stack)
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
                local_stack = self.incrementPc(local_stack)
                log(local_stack)
                
            elif bytecode["opr"] == "incr":   
                log("(incr)")
                lv_type, value = local_stack[0][bytecode["index"]]
                local_stack[0][bytecode["index"]] = (lv_type, value + bytecode["amount"])
                local_stack = self.incrementPc(local_stack)
                log(local_stack)
            elif bytecode["opr"] == "goto": 
                log("(goto)")
                local_stack = (local_stack[0], local_stack[1], (absolute_method, bytecode["target"]))
                log(local_stack)
            elif bytecode["opr"] == "if": #Collin
                log("(if)")
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
                    # init method
                    # stored in stack
                    # when all functions have been execuated, it also need to be released
                    if bytecode["method"]["name"] == "<init>":
                        local_stack[1].append(bytecode["method"]["name"])
                        log(local_stack)
                    pass
                else:
                    print("Invoke type not supported" + bytecode["access"])
            else:
                print("bytecode opr not implemented" + str(bytecode["opr"]))
                local_stack = (local_stack[0], local_stack[1], (absolute_method, local_stack[2][1] + 1))
                log(local_stack)
        return None

def traverse_files():
    path = Path("bin/course-examples/json")
    files = []
    for f in path.glob("**/Calls.json"):
        files.append(f)
    return files

def tests(f):
    #("dtu/compute/exec/Simple", "add")
    interpreter = Interpreter(f)
    data = interpreter.get_json()
    interpreter.get_classes(data)
    #testadd(interpreter)
    #testfactorial(interpreter)
    testfibonaci(interpreter)
    print("all tests fine :D")
    return

def testfibonaci(interpreter):
    case = ("dtu/compute/exec/Calls", "fib")
    testint = random.randint(1,400)
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res=interpreter.interpret(case, 0, print, memory, [("int", testint)])
    assert sympy.fibonacci(testint+1)==res

def testadd(interpreter):
    case = ("dtu/compute/exec/Simple", "add")
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    testint2 = random.randint(-sys.maxsize,sys.maxsize)
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])
    assert testint1 +testint2 == res

def testfactorial(interpreter):
    case = ("dtu/compute/exec/Simple", "factorial")
    # testint1 = random.randint(1,5)
    testint1 = 3
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1)])
    assert math.factorial(testint1) == res

def Fibonacci(n):
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return Fibonacci(n-1) + Fibonacci(n-2)

def main():
    files = traverse_files()
   
    for f in files:
        memory = {'class': [], 'array': [], 'int': [], 'float': []}
        interpreter = Interpreter(f)
        data = interpreter.get_json()
        classes = interpreter.get_classes(data)
        methods = interpreter.get_methods(classes)
        annotations = interpreter.get_annotations(methods)
        # cases = [("dtu/compute/exec/Simple", "noop"), ("dtu/compute/exec/Simple", "zero"), 
        #          ("dtu/compute/exec/Simple", "hundredAndTwo"), ("dtu/compute/exec/Simple", "identity"),
        #          ("dtu/compute/exec/Simple", "add"), 
        #          ("dtu/compute/exec/Simple", "factorial"), ("dtu/compute/exec/Calls", "fib")]

        # cases = [("dtu/compute/exec/Simple", "factorial")]
        tests(f)
        # for case in cases:
            
        #     method = interpreter.find_method(case)
        #     params = method["params"]
        #     args = []
            
        #     for param in params:
        #         if "base" in param["type"] and param["type"]["base"] == "int":
        #             # Generate random int
        #             random_int = random.randint(0, 3)
        #             args.append(("integer", random_int))
                    
        #     print("args: ", args)                      
        #     res = interpreter.interpret(case, 0, print, memory, args)
        #     print("returns: ", res)
        # classes_methods = interpreter.get_classes_methods(classes, methods)
main()

