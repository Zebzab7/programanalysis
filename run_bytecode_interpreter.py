from pathlib import Path
import json

class Interpreter:
    
    # Memory as a dictionary
    mem = {}

    # Locals, operational stack, program counter
    stack = ([], [], 0)

    # The program
    path = Path("Interpreter/")

    classes = {}
    for f in path.glob("Simple_start.json"):
        with open(f) as json_file:
            doc = json.load(json_file)
            classes[doc["name"]] = doc

    print(classes)

    

    