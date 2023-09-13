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
    
    if 'base' in field['type']:
        return field['type']['base']
    if 'kind' in field['type']:
        if(field['type']['kind'] == 'class'):
            
            if 'inner' in field['type']:
                if str(field['type']['inner']) == "None":
                    return field['type']['name']
                return field['type']['inner']['name']
                
        
        

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


for file_name in os.listdir(full_path):
    if file_name.endswith('AI.json'):
        file = open(os.path.join(full_path, file_name), 'r')
        data = json.load(file)

        # Finds methods
        json_methods = data['methods']
        methods = []
        for method in json_methods:
            name = method['name']
            if (method['access'][0] == 'public'):
                access = '+'
            else:
                access = '-'

            if ('kind' in method['returns']):
                    print(name)
                    brackets = '[]'
                    current_level = method['returns']

                    while('kind' in current_level['type']):
                        brackets += '[]'
                        current_level = current_level['type']

                    returnType = current_level['type'] + brackets
            else:
                returns = method['returns']['type']
                returnType = 'NAN'
                if (returns == None):
                    returnType = 'void'
                elif('base' in returns):
                    returnType = returns['base']
                elif('kind' in returns):
                    if (returns['kind'] == 'class'):
                        print(name)
                        returnType = returns['inner']['name']

            methods.append(access + name + '()' + ':' + returnType)
        print(methods)
  
        fieldsjson = data['fields']
        print(file_name)
        fields = {}
        if(len(fieldsjson) == 0):
            continue
        fields = simplefields(fieldsjson)
        print(fields)

    


            
        
        
        
    
