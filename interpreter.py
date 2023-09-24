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
    
    def ifstack(self, boolean, target,pc):
        if boolean:
            return target
        return pc+1
    
    def incrementPc(self,local_stack):
        absolute_method = local_stack[2][0]
        return (local_stack[0], local_stack[1], (absolute_method, local_stack[2][1] + 1))

    def interpret(self, absolute_method, pc, log):
        print("Absolute method: ", absolute_method)
        
        # λ,σ,ι
        local_stack = ([],[],(absolute_method, pc))
        # stack_list = [([],[],(absolute_method, pc))] 
        method = self.find_method(absolute_method)

        bytecode_statements = method["code"]["bytecode"]
        length = len(bytecode_statements)
        while local_stack[2][1]<length: #(i,seq[0])

            bytecode = bytecode_statements[local_stack[2][1]]
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
                log("(add)")
                if bytecode["operant"] == 'add':
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var1 + var2))
                    local_stack = self.incrementPc(local_stack)
                elif bytecode["operant"] == 'mul':
                    lv_type1, var1 = local_stack[1].pop()
                    lv_type2, var2 = local_stack[1].pop()
                    local_stack[1].append((lv_type1, var1 * var2))
                    local_stack = self.incrementPc(local_stack)
                else:
                    print("operant not supported " + bytecode["operant"])
            elif bytecode["opr"] == "store":
                log("(store)")
                lv_type, var = local_stack[1].pop()
                local_stack[0][bytecode["index"]] = var
            elif bytecode["opr"] == "incr":   
                log("(incr)")
                lv_type, value = local_stack[0][bytecode["index"]]
                local_stack[0][bytecode["index"]] = (lv_type, value + bytecode["amount"])
                local_stack = self.incrementPc(local_stack)
            elif bytecode["opr"] == "goto": 
                log("(goto)")
                local_stack = (local_stack[0], local_stack[1], (absolute_method, bytecode["target"]))
            elif bytecode["opr"] == "if": #Collin
                log("(if)")
                left,left_val = local_stack[1][-2]
                right,right_val = local_stack[1][-1]
                if bytecode["condition"] == "gt":
                    gt = left_val > right_val
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(gt, bytecode["target"],pc)))
                elif bytecode["condition"] == "lt":
                    lt = left_val < right_val
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(lt, bytecode["target"],pc)))
                elif bytecode["condition"] == "eq":
                    eq = left_val == right_val
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(eq, bytecode["target"],pc)))  
                else:
                    print("if type not implemented" + str(bytecode["condition"]))
            elif bytecode["opr"] == 'ifz': #if zero
                log("(if)")
                lv_type,val = local_stack[1][-1]
                if bytecode["condition"] == "lz":
                    lz = (val == 0)
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(lz, bytecode["target"],pc)))
                elif bytecode["condition"] == "le":
                    le = (val <= 0)
                    local_stack = (local_stack[0], local_stack[1], (absolute_method, self.ifstack(le, bytecode["target"],pc)))
                else:
                    print("ifz type not implemented" + str(bytecode["condition"]))
                pass
            elif bytecode["opr"] == "get":
                log("(get)")
                get_field = bytecode["field"]
                if "type" in get_field:
                    local_stack[1].append(get_field["type"]["name"] + get_field["name"])
                else:
                    local_stack[1].append(get_field["name"])
                local_stack = self.incrementPc(local_stack)
                pass
            elif bytecode["opr"] == "invoke":
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

