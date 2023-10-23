from pathlib import Path
from logging import log

from AbstractInterpreter import AbstractInterpreter

import json
from interpretertest import *

class Ranges():
    def __init__(self,start,end):
        self.start = start
        self.end = end
    def toString(self):
        return "start:" + str(self.start) + " end:" + str(self.end)
    
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
        return Ranges(a.start+b.start,a.end+b.end)
    def _sub(a,b):
        return Ranges(a.start-b.end,a.end-b.start)
    def _mul(a,b):
        products =[a.start*b.start,a.start*b.end,a.end*b.start,a.end*b.end]
        return Ranges(min(products),max(products))
    def _div(a,b):
        if b.start <=0 and b.end >=0:
            raise Exception("Arithmetic Exception")
        quotients =[a.start/b.start,a.start/b.end,a.end/b.start,a.end/b.end]
        return Ranges(min(quotients),max(quotients))
    def _mod(a,b): 
        if b.start > 0:  # entirely positive
            return Ranges(0, b.end - 1)
        elif b.end < 0:  # entirely negative
            return Ranges(b.end + 1, 0)
        else:  # spans zero
            return Ranges(b.start + 1, b.end - 1)

class AbstractOperations():

    def _return(self,byte,local_stack):
        
        pass
    
    def _push(self,byte,local_stack):
        value = byte["value"]["value"]
        btype = byte["value"]["type"]
        value = Ranges(value["value"],value["value"])
        return (local_stack[0],local_stack[1].append((btype, value)),local_stack[2])
    
    def _load(self,byte,local_stack):
        lv_type, value = local_stack[0][byte["index"]]
        return (local_stack[0].append((lv_type,value)),local_stack[1],local_stack[2])
    
    def _binary(self,byte,local_stack):
        byte = byte["opr"]
        lv_type1,var1 = local_stack[1].pop()
        lv_type2,var2 = local_stack[1].pop()
        if hasattr(self,"_"+byte["operant"]):
            result = getattr(self,"_"+byte["operant"])(var1,var2)
            return (local_stack[0], local_stack[1].append(lv_type1,result), local_stack[2])
        raise Exception("Binary Operant not supported " + byte["operant"])
    
    def _store(self,byte,local_stack):
        lv_type, val = local_stack[1].pop()
        if byte["index"] < len(local_stack[0]):
            new_local_var = local_stack[0][byte["index"]] = (lv_type, val)
            return (new_local_var, local_stack[1], local_stack[2])
        else: 
            new_local_var = local_stack[0].append((lv_type, val))
            return (new_local_var, local_stack[1], local_stack[2])
    
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
        var2 = Ranges(0,0)
        if hasattr(self,"_"+byte["opr"]):
            result = getattr(self,"_"+byte["opr"])(var1,var2)
            return (local_stack[0], local_stack[1], (local_stack[2][0], self.ifstack(result, byte["target"],local_stack[2][1]))) 
        raise Exception("Ifz operant not supported " + byte["opr"])
    
def traverse_files():
    path = Path("bin/course-examples/json/")
    files = []
    for f in path.glob("**/Arithmetics.json"):
        files.append(f)
    return files

def tests(interpreter):
    runAbstract(interpreter)
    print("all tests fine :D")
    return

def main():
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    files = traverse_files()
    abstract_interpreter = AbstractInterpreter()
    for f in files:
        data = abstract_interpreter.get_json(f)
        abstract_interpreter.get_class(data)
    print("Before tests")
    tests(abstract_interpreter)

main()