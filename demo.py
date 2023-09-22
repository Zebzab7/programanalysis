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
def bytecode_interpreter(am):     
   # Locals, operational stack, program counter
    methods_stack = ([], [], (am,0))
    bytecode = find_methods(am)["code"]["bytecode"]
    for i, v in enumerate(bytecode):
        (l, s, (am1,i)) = methods_stack[-1]
        # the operation that index of i
        if v["opr"] == "return":
            if v["type"] == "null":
                log("return")
            else:
                log("return "+ v["type"])
        elif v["opr"] == "push":
            log("push")
            methods_stack.append(l,s.append(v),(am,i+1))
        


                

             
