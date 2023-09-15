import json
import os
import subprocess

def find_class_files(base_path):
    class_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.class'):
                class_files.append(os.path.join(root, file))
    return class_files

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
                
def checkname(name):
    if(name == '$VALUES'):
        return "JSONERROR"
    return str(name)       

def simplefields(fieldsjson):
    
    fields = []
    for i in range(len(fieldsjson)):

        if(fieldsjson[i]['access'][0] == 'private'):
            name = fieldsjson[i]['name']
            string = "-" + checkname(name) + "() : " + str(fieldType(fieldsjson[i]))
            fields.append(string)
            
        elif(fieldsjson[i]['access'] == 'public'):
            name = fieldsjson[i]['name']
            string = "+" + checkname(name) + "() : " + str(fieldType(fieldsjson[i]))
            fields.append(string)
            
        elif(fieldsjson[i]['access'] == 'protected'):
            name = fieldsjson[i]['name']
            string = "#" + checkname(name) + "() : " + str(fieldType(fieldsjson[i]))
            fields.append(string)
        
    return fields

# returns a string representation of the objects parameters
def getObjectParameters(object):
    params_string = ''
    if ('params' in object):
        params = object['params']
        if (params != None and len(params) > 0):
            params = object['params']
            for i in range(len(params)):
                params_string += getObjectType(params[i])
                if (i < len(params) - 1):
                    params_string += ','
            return params_string
    return ''

# returns a string representation of the objects type
def getObjectType(object):
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
        elif(objectType['kind'] == 'array'):
            result = getObjectType(objectType) + '[]'

    return result


directory = os.path.dirname(__file__)
# relative_path = "AI-assignments/Classes/student/dtu"
project_name = "AI-assignments"
path_to_class_files = project_name + "/KalahaAI/bin"

full_path = os.path.join(directory, path_to_class_files)

class_files = find_class_files(path_to_class_files)
print(class_files)

for file in class_files:
    # find and remove last file in directory:
    trimmed_class_path = file.rsplit('/', 1)[0] + "/"
    # find file name without .class
    file_name = file.rsplit('/', 1)[1].split('.')[0]
    # Remove dollar signs:
    file_name = file_name.replace('$', '')
    # if directory does not exist, create it
    path_to_json = "bin/" + project_name + "/json"
    if not os.path.exists(path_to_json):
        os.makedirs(path_to_json)
    # run jvm2json on file
    command = "jvm2json -s " + file + " -t " + path_to_json + "/" + file_name + ".json"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

fields = []
filenameArr = []

for file_name in os.listdir(path_to_json):
    if(file_name.endswith('.class')):
        continue
    filenameArr.append(file_name)
    file = open(os.path.join(path_to_json, file_name), 'r',encoding='utf-8',errors='ignore')
    data = json.load(file)
    
    methods = []
    print(file_name)

    # Finds methods
    json_methods = data['methods']
    for method in json_methods:
        name = method['name']
        if (name != '<init>' and name != '<clinit>'): 
            if (method['access'][0] == 'public'):
                access = '+'
            else:
                access = '-'
            params_string = getObjectParameters(method)
            returns = method['returns']
            returnType = getObjectType(returns)
            methods.append(access + name + '(' + params_string + ')' + ':' + returnType)
        fieldsjson = data['fields']
        if(len(fieldsjson) == 0):
            continue
        fields.append(simplefields(fieldsjson))
    print(methods, "\n")
        