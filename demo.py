from logging import log
from pathlib import Path
import json

path = Path("//Users/chenyang/Desktop/CoursesMaterials/ProgramAnalysis/assign3/programanalysis/bin/course-examples/json/")

classes = {}
# Memory as a dictionary
mem = {}





for f in path.glob("Simple.json"):
    with open(f) as json_file:
        doc = json.load(json_file)
        classes[doc["name"]] = doc

# print(classes.values())

cases= []

# find all the test methods
for cls in classes.values():
    for method in cls["methods"]:
        for anno in method["annotations"]:
            if anno["type"] == "dtu/compute/exec/Case":
                cases.append(method)

# find methods
def find_methods(am):
    print(am[0])
    ms = classes[am[0]]["methods"]
    for m in ms:
        if m["name"] == am[1]:
            return m
        

# find_bytecode
def find_bytecode(am):
    m = find_methods(am)
    assert m is not None
    print(m["code"]["bytecode"])

# find_bytecode(("dtu/compute/exec/Simple","noop"))


# interpreter
bytecode_info = ("offset","opr","type")
def bytecode_interpreter(am):     
    # Locals, operational stack, program counter
    methods_stack = ([], [], (am,0))
    bytecode = find_methods(am)["code"]["bytecode"]
    
    # store all the local variables in an array --lambda
    # not sure--not clear about "localVariables"
    method_code = find_methods(am)['code']
    if  method_code["stack_map"] is not None and "locals" in method_code["stack_map"]:
        methods_stack = list(methods_stack)
        for local in method_code["stack_map"]["locals"]:
            methods_stack[0].append(local)
        methods_stack = tuple(methods_stack)
        

    for i, v in enumerate(bytecode):
        (l, s, (am1,i)) = methods_stack[-1]
        # the operation that index of i
        # different operation {load,return,push,binary,if,goto,store,incr...}
        # basic key in bytecode {offset,opr,type}
        if v["opr"] == "return":
            if v["type"] == "null":
                log("return")
            else:
                log("return "+ v["type"])
        elif v["opr"] == "push":
            log("push")
            methods_stack.append(l,s.append(v["value"]),(am,i+1))
        elif v["opr"] == "load":
            log("load parameter"+ v["type"])
        elif "target" in v:
            l[v["target"]]
           
            
            
        

        
        


                

             
