import json
import os

directory = os.path.dirname(__file__)
relative_path = "AI-assignments/Classes/student/dtu"
full_path = os.path.join(directory, relative_path)

def printGraph(graph):
    if os.path.exists("graph.dot"):
        os.remove("graph.dot")
    # Create a new file
    f = open("graph.dot", "a")


def graphfields(self,fields):
    return

def fieldType(field):
    field = field['type']
    if 'base' in field:
        return field['base']
    if 'kind' in field:
        if(field['kind'] == 'class'):
            
            if 'inner' in field:
                if str(field['inner']) == "None":
                    return field['name']
                return field['inner']['name']
                


def simplefields(fieldsjson):

    fields = []
    for i in range(len(fieldsjson)):

        if(fieldsjson[i]['access'][0] == 'private'):
            name = fieldsjson[i]['name']
            string = "-" + str(name) + "() : " + str(fieldType(fieldsjson[i]))
            fields.append(string)
            
        elif(fieldsjson[i]['access'] == 'public'):
            name = fieldsjson[i]['name']
            string = "+" + str(name) + "() : " + str(fieldType(fieldsjson[i]))
            fields.append(string)
            
        elif(fieldsjson[i]['access'] == 'protected'):
            name = fieldsjson[i]['name']
            string = "#" + str(name) + "() : " + str(fieldType(fieldsjson[i]))
            fields.append(string)
        
    return fields

def getObjectType(object):
    print(object)
    objectType = object['type']
    result = "NAN"
    if (objectType == None):
        result = 'void'
    elif('base' in objectType):
        result = objectType['base']
    elif('kind' in objectType):
        if (objectType['kind'] == 'class'):
            if (objectType['inner'] == None):
                #Trim away all '/' and only include last part of name
                result = objectType['name'].split('/')[-1]
            else:
                currentLayer = objectType['inner']
                result = currentLayer['name']
                while (currentLayer['inner'] != None):
                    currentLayer = currentLayer['inner']
                    result += currentLayer['name']
            args = objectType['args']
            if (args != None and len(args) > 0):
                if (len(args) == 1):
                    result += '<' + getObjectType(args[0]) + '>' 
                else: 
                    result += '<'
                    for i in range(len(args)):
                        result += getObjectType(args[i])
                        if (i < len(args) - 1):
                            result += ','
                    result += '>'
    return result

fields = []
methods = []
filenameArr = []

for file_name in os.listdir(full_path):
    if(file_name.endswith('.class')):
        continue
    filenameArr.append(file_name)
    file = open(os.path.join(full_path, file_name), 'r',encoding='utf-8',errors='ignore')
    data = json.load(file)

    if (file_name.endswith('AINode.json')):
        # Finds methods
        json_methods = data['methods']
        for method in json_methods:
            name = method['name']
            print(name)
            if (method['access'][0] == 'public'):
                access = '+'
            else:
                access = '-'
            returns = method['returns']
            returnType = getObjectType(returns)
            print(returnType)
            methods.append(access + name + '()' + ':' + returnType)
            fieldsjson = data['fields']
            if(len(fieldsjson) == 0):
                continue
            fields.append(simplefields(fieldsjson))
        print(methods)
        

    


            
        
        
        
    
