from pathlib import Path
import json

  
mem = {}
# Memory as a dictionary
# Locals, operational stack, program counter
stack = ([], [], 0)

def checkNOOP(b):
    keys = ["offset", "opr", "type"]
    for key in keys:
        if key not in b:
            return False
    return (b["offset"] == 0 and str(b["opr"]) == "return" and str(b["type"]) == "None")

# The program
path = Path("bin/course-examples/json")

cases = []
classes = {}
for f in path.glob("**/Simple.json"):
    with open(f) as json_file:
        doc = json.load(json_file)
        classes[doc["name"]] = doc
    
# The program
    
for cls in classes.values():
    for method in cls["methods"]:
        for annotation in method["annotations"]:
            if annotation["type"] == "dtu/compute/exec/Case":
                cases.append(method)

# am is absolute method and is structured such that 
# am[0] = class name and am[1] = method name
def find_method(am):
    ms = classes[am[0]]["methods"]
    for m in ms:
        if m["name"] == am[1]:
            return m
        

        
# The program
for cls in classes.values():
    for method in cls["methods"]:

        for annotation in method["annotations"]:
            if annotation["type"] == "dtu/compute/exec/Case":
                cases.append(method)



def interpreter(am):
    # Memory as a dictionary
    mem = {}
    # Locals, operational stack, program counter
    stack = [([], [], (am, 0))]

    print(am)
    method = find_method(am)
    bytecode = method["code"]["bytecode"]
    for i in range(len(bytecode)):
        (ls, os, (am_, i)) = stack[-1]
        b = bytecode[i]
        if(checkNOOP(b)):#TODO: PUSH PC by 1 maybe
            print("NOOP at " + str(i))
        # TODO 
        # handle_operation(b, stack)

cn = "dtu/compute/exec/Simple"
func = cases[0]
interpreter((cn, func["name"]))
