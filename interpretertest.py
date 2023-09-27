import sys
import math
import sympy
import random
def testmin(interpreter):
    case = ("dtu/compute/exec/Simple", "min")
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    testint2 = random.randint(-sys.maxsize,sys.maxsize)
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])    
    assert min(testint1,testint2) == res, str(testint1) + " " + str(testint2) + " " + str(res)

def testfibonaci(interpreter):
    case = ("dtu/compute/exec/Calls", "fib")
    testint = 4
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res=interpreter.interpret(case, 0, print, memory, [("int", testint)])
    assert sympy.fibonacci(testint+1)==res , str(testint+1) + " " + str(res)

def testadd(interpreter):
    case = ("dtu/compute/exec/Simple", "add")
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    testint2 = random.randint(-sys.maxsize,sys.maxsize)
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])
    assert testint1 +testint2 == res, str(testint1) + " " + str(testint2) + " " + str(res)

def testfactorial(interpreter):
    case = ("dtu/compute/exec/Simple", "factorial")
    # testint1 = random.randint(1,5)
    testint1 = 3
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1)])
    assert math.factorial(testint1) == res, str(testint1) + " " + str(res)
def testNoop(interpreter):
    case = ("dtu/compute/exec/Simple", "noop")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert res == None, str(res) + " " + str(None)
def testZero(interpreter):
    case = ("dtu/compute/exec/Simple", "zero")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert res == 0, str(res) + " " + str(0)
def testHundredAndTwo(interpreter):
    case = ("dtu/compute/exec/Simple", "hundredAndTwo")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert res == 102, str(res) + " " + str(102)
def testIdentity(interpreter):
    case = ("dtu/compute/exec/Simple", "identity")
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1)])
    assert res == testint1, str(res) + " " + str(testint1)

def alwaysThrows1(interpreter,exceptiontype):
    
    case = ("eu/bogoe/dtu/Arithmetic", "alwaysThrows1")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory,[("int", testint)])
    assert "Yes" == res, "Yes " + res

def alwaysThrows2(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "alwaysThrows2")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint = random.randint(-sys.maxsize,sys.maxsize)
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert "Yes" == res, "Yes " + res

def alwaysThrows3(interpreter,exceptiontype): ##Why does this always throw
    case = ("eu/bogoe/dtu/Arithmetic", "alwaysThrows3")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testfloat1 = float(random.randint(-sys.maxsize,sys.maxsize))
    testfloat2 = float(random.randint(-sys.maxsize,sys.maxsize))
    type_,res = interpreter.interpret(case, 0, print, memory, [("float", testfloat1),("float", testfloat2)])
    assert "Yes" == res, "Yes " + res

def alwaysThrows4(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "alwaysThrows4")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    testint2 = 0
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])
    assert "Yes" == res, "Yes " + res

def alwaysThrows5(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "alwaysThrows5")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    testint2 = random.randint(-sys.maxsize,sys.maxsize)
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])
    assert "Yes" == res, res

def itDependsOnLattice1(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "itDependsOnLattice1")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert "Yes" == res | "No" == res, "Both " + res

def itDependsOnlattice2(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "itDependsOnLattice2")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert "Yes" == res | "No" == res, "Both " + res

def itDependsOnlattice3(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "itDependsOnLattice3")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint1 = random.randint(1001,sys.maxsize)
    testint2 = random.randint(11,sys.maxsize)
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])
    assert "Yes" == res | "No" == res, "Both " + res

def neverThrows1(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "neverThrows1")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert "No" == res, "No " + res

def neverThrows2(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "neverThrows2")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1)])
    assert "No" == res, "No " + res

def neverThrows3(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "neverThrows3")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint1 = random.randint(1,sys.maxsize)
    testint2 = 0
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])
    assert "No" == res, "No " + res

def neverThrows4(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "neverThrows4")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1)])
    assert "No" == res, "No " + res

def neverThrows5(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "neverThrows5")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    testint1 = random.randint(-sys.maxsize,sys.maxsize)
    testint2 = random.randint(-sys.maxsize,sys.maxsize)
    type_,res = interpreter.interpret(case, 0, print, memory, [("int", testint1),("int", testint2)])
    assert "No" == res, "No " + res

def speedVsPrecision(interpreter,exceptiontype):
    case = ("eu/bogoe/dtu/Arithmetic", "speedVsPrecision")
    memory = {'class': [], 'array': [], 'int': [], 'float': []}
    type_,res = interpreter.interpret(case, 0, print, memory, [])
    assert "Yes" == res | "No" == res, "Both " + res

def runConcrete(interpreter):
    testmin(interpreter)
    testfibonaci(interpreter)
    testadd(interpreter)
    testfactorial(interpreter)
    testNoop(interpreter)
    testZero(interpreter)
    testHundredAndTwo(interpreter)
    testIdentity(interpreter)
