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
bytecodes = []
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
                bytecodes.append(method["code"]["bytecode"])

        
for method in cases:
    print(method["name"])
    #print(method["code"]["bytecode"])
    b = method["code"]["bytecode"]
    for i in range(len(b)):
        if(checkNOOP(b[i])):#TODO: PUSH PC by 1 maybe
            print("NOOP at " + str(i))
        
