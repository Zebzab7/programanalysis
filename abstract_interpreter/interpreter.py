import json
from pathlib import Path
from logging import log
from interpretertest import *
import sys
from RangesR import Ranges_abstract

class AbstractInterpreter:

    def __init__(self,k):
        self.classes = {}
        self.memory = {}
        self.kCounterMax = k
        self.kCounter = 0

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
        
        # local_variables = []

        # for i in range(10):
        #     local_variables.append(None)


        # λ,σ,ι
        local_stack = ([None, None], [],(absolute_method, pc))
        method = self.find_method(absolute_method)
        if method == absolute_method[1]:
            log("executing method: ", absolute_method[1], " with arguments: ", args)
            # return None,None

        # Load in arguments
        # if len(args) <= 2:
        for i in range(len(args)):
            local_stack[0][i] = args[i]

        bytecode_statements = method["code"]["bytecode"]
        length = len(bytecode_statements)
        while local_stack[2][1]<length: #(i,seq[0])
            pc = local_stack[2][1] #PC
            bytecode = bytecode_statements[pc]
            if bytecode["opr"] == "return":
                log("(return)")
                local_stack = AbstractOperations._return(self, bytecode, local_stack)
                log(local_stack)
                return local_stack
            elif bytecode["opr"] == "push":
                log("(push)")
                local_stack = AbstractOperations._push(self, bytecode, local_stack)
            elif bytecode["opr"] == "load":  
                log("(load)")
                local_stack = AbstractOperations._load(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "binary": 
                log("(binary)")
                local_stack = AbstractOperations._binary(self, bytecode, local_stack)
                if(local_stack == None):
                    return None, "Arithmetic Exception Raised"
                log(local_stack)
            elif bytecode["opr"] == "store":
                log("(store)")
                local_stack = AbstractOperations._store(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "incr":   
                log("(incr)")
                local_stack = AbstractOperations._incr(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "goto": 
                log("(goto)")
                local_stack = AbstractOperations._goto(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "if": #Collin
                log("(if)")
                local_stack = AbstractOperations._if(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == 'ifz': #if zero
                log("(ifz)")
                local_stack = AbstractOperations._ifz(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "get":
                log("(get)")
                local_stack = AbstractOperations._get(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "invoke":
                log("(invoke)")
                local_stack = AbstractOperations._invoke(self, bytecode, local_stack)
                log(local_stack)
            local_stack=self.incrementPc(local_stack)
            if(self.kCounter==self.kCounterMax):
                return self.kCounter, "K counter reached"
            self.kCounter = self.kCounter + 1 
        return None
    
class Comparison():
    def _eq(a,b):
        return a==b
    def _ne(a,b):
        return a!=b
    def _ge(a,b):
        return a>=b
    def _gt(a,b):
        return a>b
    def _lt(a,b):
        return a<b
    #THESE two are not supported in java
    def _is(a,b):
        return a is b
    def _isnot(a,b):
        return a is not b
    
#if a,b
#ifz a,0
class AbstractComparison():
    def _eq(a,b):
        return (a.start == b.start and a.end == b.end)
    def _ne(a,b):
        return (a.start != b.start and a.end != b.end)
    def _ge(a,b):
        return (a.start >= b.start and a.end >= b.end)
    def _gt(a,b):
        return (a.start > b.start and a.end > b.end)
    def _lt(a,b):
        return (a.start < b.start and a.end < b.end)    
    #These are not supported in java, also what would they do in a abstract sense?
    def _is(a,b):
        print("Not supported, IS")
    def _isnot(a,b):
        print("Not supported, Is Not")

class ArithmeticOperations():
    def _add(a,b):
        return a+b
    def _sub(a,b):
        return a-b
    def _mul(a,b):
        return a*b
    def _div(a,b):
        return a//b
    def _mod(a,b):
        return a%b
    #Not supported in java
    def _expo(a,b):
        return a**b
    
class AbstractArithmeticOperations():
    def _add(a,b):
        return Ranges_abstract(a.start+b.start,a.end+b.end)
    def _sub(a,b):
        newrange = Ranges_abstract(a.start-b.end,a.end-b.start)
        return newrange
    def _mul(a,b):
        products =[a.start*b.start,a.start*b.end,a.end*b.start,a.end*b.end]
        return Ranges_abstract(min(products),max(products))
    def _div(a,b):
        if b.start <=0 and b.end >=0:
            return 'Arithmetic exception raised'
        quotients =[a.start//b.start,a.start//b.end,a.end//b.start,a.end//b.end]
        return Ranges_abstract(min(quotients),max(quotients))
    def _mod(a,b): 
        if b.start > 0:  # entirely positive
            return Ranges_abstract(0, b.end - 1)
        elif b.end < 0:  # entirely negative
            return Ranges_abstract(b.end + 1, 0)
        else:  # spans zero
            return Ranges_abstract(b.start + 1, b.end - 1)

class AbstractOperations():

    def _return(self,byte,local_stack):
        if byte["type"] == None:
            log("(return) None")
            return None
        elif byte["type"] == "int":
            log("(return) int: ", local_stack[1][-1])
            return local_stack[1][-1] #Returns the last element in the opr. stack
        elif byte["type"] == "float":
            log("(return) float: ", local_stack[1][-1])
            return local_stack[1][-1]
        else:
            log("return type not implemented "+ byte["type"])
        pass
    
    def _push(self,byte,local_stack):
        value = byte["value"]["value"]
        btype = byte["value"]["type"]
        value = Ranges_abstract(value,value)
        local_stack[1].append((btype, value))
        print(local_stack)
        return local_stack
    
    def _load(self,byte,local_stack):
        print(local_stack[0])
        print(byte["index"])
        lv_type, value = local_stack[0][byte["index"]]
        local_stack[1].append((lv_type,value))
        print(local_stack)
        return local_stack
    
    def _binary(self,byte,local_stack):
        lv_type1,var2 = local_stack[1].pop()
        lv_type2,var1 = local_stack[1].pop()
        if hasattr(AbstractArithmeticOperations,"_"+byte["operant"]):
            print(var1.toString(),var2.toString())
            result = getattr(AbstractArithmeticOperations,"_"+byte["operant"])(var1,var2)
            if(result == 'Arithmetic exception raised'):
                return None
            local_stack[1].append((lv_type1,result))
            return local_stack
        raise Exception("Binary Operant not supported " + byte["operant"])
    
    def _store(self,byte,local_stack):
        lv_type, val = local_stack[1].pop()      
        local_stack[0][byte["index"]] = (lv_type, val)
        return local_stack
    
    def _incr(self,byte,local_stack):
        lv_type, value = local_stack[0][byte["index"]]
        value.start = value.start + byte["amount"]
        value.end = value.end + byte["amount"]
        local_stack[0][byte["index"]] =(lv_type,value)
        return local_stack
    
    def _get(self,byte,local_stack):
        print("Not implemented get")
        pass
    
    def _goto(self,byte,local_stack):
        return (local_stack[0],local_stack[1],(local_stack[2][0],byte["target"]-1))
            
    def _if(self,byte,local_stack):
        lv_type1,var1 = local_stack[1].pop()
        lv_type2,var2 = local_stack[1].pop()
        if hasattr(self,"_"+byte["opr"]):
            result = getattr(self,"_"+byte["opr"])(var1,var2)
            return (local_stack[0], local_stack[1], (local_stack[2][0], self.ifstack(result, byte["target"],local_stack[2][1])))
        raise Exception("If operant not supported " + byte["opr"])
    
    def _ifz(self,byte,local_stack):
        lv_type1,var1 = local_stack[1].pop()
        var2 = Ranges_abstract(0,0)
        if hasattr(self,"_"+byte["opr"]):
            result = getattr(self,"_"+byte["opr"])(var1,var2)
            return (local_stack[0], local_stack[1], (local_stack[2][0], self.ifstack(result, byte["target"],local_stack[2][1]))) 
        raise Exception("Ifz operant not supported " + byte["opr"])
    
def traverse_files():
    source_to_files = "../bin/course-examples/json/"
    working_path = Path(__file__).parent
    json_files = (working_path / source_to_files).resolve()
    path = Path(json_files)
    print(path)
    files = []
    for f in path.glob("**/Arithmetics.json"):
        files.append(f)
    if len(files) == 0:
        print("No files found")
        sys.exit()
    return files

def tests(interpreter):
    runAbstract(interpreter)
    print("all tests fine :D")
    return

def main():
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    files = traverse_files()
    k= 1000
    abstract_interpreter = AbstractInterpreter(k)
    for f in files:
        data = abstract_interpreter.get_json(f)
        abstract_interpreter.get_class(data)
        
    print("Before tests")
    tests(abstract_interpreter)
    

main()

