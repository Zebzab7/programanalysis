from interpreter_abstract import AbstractOperations

class AbstractInterpreter:

    def __init__(self):
        self.classes = {}
        self.memory = {}

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

        # λ,σ,ι
        local_stack = ([],[],(absolute_method, pc))
        method = self.find_method(absolute_method)
        if method == absolute_method[1]:
            log("executing method: ", absolute_method[1], " with arguments: ", args)
            # return None,None

        # Load in arguments
        for arg in args:
            local_stack[0].append(arg)

        bytecode_statements = method["code"]["bytecode"]
        length = len(bytecode_statements)
        while local_stack[2][1]<length: #(i,seq[0])
            pc = local_stack[2][1] #PC
            bytecode = bytecode_statements[pc]
            if bytecode["opr"] == "return":
                log("(return)")
                if bytecode["type"] == None:
                    log("(return) None")
                    return None
                elif bytecode["type"] == "int":
                    log("(return) int: ", local_stack[1][-1])
                    return local_stack[1][-1] #Returns the last element in the opr. stack
                else:
                    log("return type not implemented "+ bytecode["type"])
                log(local_stack)
            elif bytecode["opr"] == "push":
                log("(push)")
                local_stack = AbstractOperations._push(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "load":  
                log("(load)")
                local_stack = AbstractOperations._load(self, bytecode, local_stack)
                log(local_stack)
            elif bytecode["opr"] == "binary": 
                log("(binary)")
                local_stack = AbstractOperations._binary(self, bytecode, local_stack)
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
        return None