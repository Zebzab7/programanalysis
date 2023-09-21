from pathlib import Path
import json

class Interpreter:
    def __init__(self, json_file):
        self.json_file = json_file

    def get_json(self):
        with open(self.json_file) as f:
            data = json.load(f)
        return data
    
    #Get all class names 
    def get_classes(self, data):
        classes = {}
        classes[data["name"]] = data
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

        classes_methods = interpreter.get_classes_methods(classes, methods)

main()