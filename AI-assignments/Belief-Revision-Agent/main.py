#main class
from sympy.logic.boolalg import to_cnf
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent
from sympy import *
import traceback
import re #RegEx
Belief_base = [] #Made of tuples (Expression, Priority)

def main():
    #To stop local ref errors
    global Belief_base
    initial_belief_base()
    while(True):
        print("Enter 1. to revise belief base with a new belief")
        print("Enter 2. to contract a belief from the belief base")
        print("Enter 3. to enter view the belief base")
        print("Enter 4. to check if the belief base entails a belief")
        print("Enter 5. to Terminate the program")


        inputx = input()
        if(inputx == "1"):
            addNewBelief()
            continue
        elif(inputx == "2"):
            contractNewBelief()
            continue
        elif(inputx == "3"):
            print(Belief_base)
            continue
        elif(inputx == "4"):
            entailment_setup()
            continue
        elif(inputx == "5"):
            break
        else:
            print("Invalid input, please try again")

def addNewBelief():
   global Belief_base
   while(True):
       print("Please enter a logical expression: ")
       x = input ()
       try:
            sentence_to_revise_by = (parse_expr(x),enterPriority())
            break
       except:
            traceback.print_exc()
            print("Invalid input, please try again")
            continue #continue to next iteration of loop
   revise_belief_base(sentence_to_revise_by)


def contractNewBelief():
   global Belief_base
   while(True):
       print("Please enter a logical expression: ")
       x = input ()
       try:
            sentence_to_contract = parse_expr(x)
            break
       except:
            traceback.print_exc()
            print("Invalid input, please try again")
            continue #continue to next iteration of loop
   if entails([],~sentence_to_contract):
        print("The belief that was to be contracted is a contradiction and therefore the belief base is not changed")
        return
   contract_belief_base(sentence_to_contract)  



def enterPriority():
    while(true):
        print("Please enter a Priority: ")
        x = input()
        if(x == "end"):
            break
        elif(x.isnumeric()):
            try:
                return int(x)
            except:
                traceback.print_exc()
        else:
            print("None number entered, try again")

def entailment_setup():
    Kb = [t[0] for t in Belief_base]
    while(True):  # Q v P & ~Q v ~P (factor) Q v ~Q
        print("Enter logical expression to see if the knowledge base entails it: ")
        alpha = input()
        if(alpha == "end"):
            break
        else:
            try:
                sentence = parse_expr(alpha)
                break
            except:
                traceback.print_exc()
                print("Invalid input, please try again")
                continue #continue to next iteration of loop
    print("KnowledgeBase and ~alpha as clauses")
    print(Kb + [~sentence])
    print("KnowledgeBase entails alpha: " + str(entails(Belief_base,sentence)))

def contains(find,list):
    if(len(list)==0):
        return False
    for i in list:
        if(i==find):
            return True
    return False


def entails(kb,sentence):
    #list of beliefs without priorities
    beliefs = [t[0] for t in kb]
    beliefs.append(~sentence) #Not sentence to entail
    clauses = to_clauses(beliefs)
    changed = True
    while(changed):
        changed = False
        for i in clauses[:]:
            for j in clauses[:]:
                if(i == j):
                    continue
                result = resolve(i,j)
                if(result == ""):
                    return True
                elif(result == "Nothing to resolve"):
                    continue
                else:
                    if(parse_expr(result) in clauses):
                        continue
                    clauses.append(parse_expr(result))
                    changed = True
    return False


def resolve(clause1, clause2):
    litterals1 = str(clause1).split(" | ") #spaces because to_cnf adds spaces
    litterals2 = str(clause2).split(" | ")
    resolution = False
    for i in litterals1[:]:
        if(bool(re.search("~",i))):
            symbol = i[1:]
        else:
            symbol = "~"+ i
        if(symbol in litterals2):
            resolution = True
            litterals1.remove(i)
            litterals2.remove(symbol)
            break
        
    if(resolution == False):
        return "Nothing to resolve"
    elif(len(litterals1) + len(litterals2) == 0):
        return ""
    else:
        combine = litterals1 + litterals2
        result = combine.pop()
        while len(combine) != 0:
            result += "|" + combine.pop()
        return result


def contract_belief_base(sentence_to_contract):
    global Belief_base
    kb = Belief_base.copy()
    temp_list_of_lists = [kb]
    remainders = []
    resolved = False
    #Vacuity check
    if not entails(kb,sentence_to_contract):
       return
    while not resolved:
        for i in temp_list_of_lists[:]:
            for j in i:
                tempset = i.copy()
                tempset.remove(j)
                if not entails(tempset,sentence_to_contract):
                    if(tempset not in remainders):
                        remainders.append(tempset)
                    resolved = True
                else:
                    if(tempset not in temp_list_of_lists):
                        temp_list_of_lists.append(tempset)
            temp_list_of_lists.remove(i)
    print("Beliefs removed by contraction: ")
    for i in remainders:
        print(i)
    if len(remainders) > 1:
        max = remainders[0]
        priority = 0
        tempPriority = 0
        for i in max:
            priority += i[1]
        for i in remainders[1:]:
            tempPriority = 0
            for j in i:
                tempPriority += j[1]
            if tempPriority > priority:
                max = i
                priority = tempPriority
        for i in Belief_base:
            if(i not in max):
                print("Removed from KB: " + str(i))
        Belief_base = max
    else:
        for i in Belief_base:
            if(i not in remainders[0]):
                print("Removed from KB: " + str(i))
        Belief_base = remainders[0]

def expand_belief_base(sentence_to_expand):
    Belief_base.append(sentence_to_expand)
    print("Belief base after expansion:")
    print(Belief_base)

def revise_belief_base(tuple_to_revise_by):
    if entails([],~tuple_to_revise_by[0]):
        print("The belief that was to be revised is a contradiction and therefore the belief base will be inconsistent")
        expand_belief_base(tuple_to_revise_by)
        return
    elif(entails([],tuple_to_revise_by[0])):
        print("The belief that was to be revised with is a tautology therefore contraction is skipped")
        expand_belief_base(tuple_to_revise_by)
        return
    contract_belief_base(~tuple_to_revise_by[0])
    expand_belief_base(tuple_to_revise_by)

def initial_belief_base():
    Belief_base.append(to_cnf((parse_expr("p >> q"),2)))
    Belief_base.append(to_cnf((parse_expr("~p >> q"),2)))
    #Belief_base.append(to_cnf((parse_expr("p & q"),2)))
    Belief_base.append(to_cnf((parse_expr("p"),2)))
    Belief_base.append(to_cnf((parse_expr("q"),2)))
    #Belief_base.append(to_cnf((parse_expr("r"),3)))
    #Belief_base.append(to_cnf((parse_expr("p & q"),2)))
    #Belief_base.append(to_cnf((parse_expr("p | q"),2)))
    Belief_base.append(to_cnf((parse_expr("(p >> q) & (q >> p)"),2)))
    #Belief_base.append(to_cnf((parse_expr("q >> p"),3)))
    #Belief_base.append(to_cnf((parse_expr("~p"),1)))
    #Belief_base.append(to_cnf((parse_expr("(p|q)>>r"),1)))
    #Belief_base.append(to_cnf((parse_expr("(~r&p)|(r&q)"),2)))

#Breaks it to minimal size by removing AND
def to_clauses(KB):
    tempBase = []

    for i in KB:
        temp = str(to_cnf(i)).split("&")
        for j in temp:
            tempBase.append(j)


    KB.clear()
    
    for i in tempBase:
        KB.append(parse_expr(i))
    return KB



main()