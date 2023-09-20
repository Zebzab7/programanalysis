from pathlib import Path
import json

# Memory as a dictionary
mem = {}

# Locals, operational stack, program counter
stack = ([], [], 0)

# The program
path = Path("bin/course-examples/json")
cases = []
bytecodes = []
classes = {}
for f in path.glob("**/Simple.json"):
    with open(f) as json_file:
        doc = json.load(json_file)
        classes[doc["name"]] = doc

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
                bytecodes.append(method["code"]["bytecode"])

# for method in cases:
#     print(method["name"])
#     print(method["code"]["bytecode"])

# print(classes["dtu/compute/exec/Simple"]["name"])

print(find_method(("dtu/compute/exec/Simple", "noop")))