# class StateAttribute():
#     #  State('state', identifier='', value='', initial=True)
#     def __init__(self,opr,value):
#         # h,bc,opr,name?
#         self.opr = opr
#         self.value = value
#         self.name = opr+value
        

class StateMachine():
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.current_state = None
        self.symbolList = []

    def add_state(self, state,symbols):
        self.states.add(state)
        for i in symbols:
            self.symbolList.append(i)

    def set_initial_state(self, state):
        if state in self.states:
            self.current_state = state
        else:
            raise ValueError(f"State {state} not found in states")

    def add_transition(self, from_state, to_state, input_symbol):
        if from_state not in self.states or to_state not in self.states:
            raise ValueError("From and to states must be in states")
        self.transitions[(from_state, input_symbol)] = to_state

    def process_input(self, input_symbol):
        if (self.current_state, input_symbol) in self.transitions:
            self.current_state = self.transitions[(self.current_state, input_symbol)]
        else:
            raise ValueError(f"No transition for input symbol {input_symbol} in current state {self.current_state}")

    def get_current_state(self):
        return self.current_state, self.symbolList

 # Given a method m and sets of initial states S1


addMachine = StateMachine()
addMachine.set_initial_state("+")

ArithmeticLattice = {"+-0","+-","+","-","0","0-","+0"}


	# public static int test() {
	# 	int i = 0;
    #   int j = 3;
    #   int k = i + j;
	# }

# "+" and "0" -> "ADD" -> "+"


#         ["-0"]
#         ^  
#         |    
#       ["0"]           ["-"]
#       "0" -> "0"

AddOptionsLattice = {"+-0": ("ADD", "+-0") ,"+-":("ADD","+-"),"+0":("ADD","+"),"+":("ADD","+"),"-":("ADD","+-0"),"0":("ADD","+"),"0-":("ADD","+-0")}

MulOptionsLattice = {"+-0": ("MUL", "+-0") ,"+-":("MUL","+-"),"+0":("MUL","+"),"+":("MUL","+"),"-":("MUL","+-0"),"0":("MUL","+"),"0-":("MUL","+-0")}

Options = dict()
Options["ADD"] = AddOptionsLattice
Options["MUL"] = MulOptionsLattice


