from statemachine import StateMachine, State


initialStateSet = {}
class State():
    # create states
    def createState(self,opr):
        if opr=="get":
            statename = State(opr,intial = True)
        elif opr=="throw":
            statename = State(opr,inital = False)
        elif opr:
            pass
    
        statename = State(opr)
        return statename

    def transitionState(fromState,toState):
        transiName = fromState.to(toState)
        return transiName
    
oprSet = ["add","mul",".."]
# if add
addAbstraction = {"-","add","+",{"-","add"},{"-","+"},{"add","+"},{"-","add","+"}}
mulAbstraction = {"-","mul","+",{"-","mul"},{"-","+"},{"mul","+"},{"-","mul","+"}}
divAbstraction = {""}
oprSet["add"] = addAbstraction
oprSet["mul"] = mulAbstraction

# traverse the method and store new state

    

    


        