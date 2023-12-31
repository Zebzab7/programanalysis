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

def legend(f):
    f.write("subgraph cluster {\n")
    f.write("j->k[label=\" dependency\",arrowhead=vee]\n")
    f.write("g->h[label=\" composition\",arrowhead=odiamond]\n")
    f.write("e->f[label=\" aggregation\",arrowhead=odot]\n")
    f.write("c->d[label=\" realization\",arrowhead=dot]\n")
    f.write("a->b[label=\" inheritance\",arrowhead=crow]\n")
    f.write("}\n")

def setup(f):
    f.write("node [shape=record style=filled fillcolor = gray95]\n")
    f.write("edge [fontname=\"Helvetica,Arial,sans-serif\"]\n")

def stringReplace(name):
    name = name.replace("$","\"$\"")
    name = name.replace("<","")
    name = name.replace(">", "")
    name = name.replace("Node","\"Node\"")
    #name = name.replace("[]","\"[]\"")
    name = name.replace("$","")
    return name

def makeGraphNode(f,file_name,methods,fields):
    file_name = file_name.replace('.json', '')
    f.write(file_name + "[label= <{<b>" + file_name + "</b>|")
    for field in fields:
        f.write(stringReplace(str(field)) + "<br align=\"left\"/>")
    f.write("|")
    for method in methods:
        f.write(stringReplace(str(method)) + "<br align=\"left\"/>")
    f.write("}>]\n")

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

project_name = "AI-assignments"
path_to_class_files = project_name + "/KalahaAI/bin"

class_files = find_class_files(path_to_class_files)
print(class_files)

for file in class_files:
    # find file name without .class
    old_file_name = file.rsplit('/', 1)[1].split('.')[0]
    # Remove dollar signs:
    file_name = old_file_name.replace('$', '')
    
    # if directory does not exist, create it
    path_to_json = "bin/" + project_name + "/json"
    if not os.path.exists(path_to_json):
        os.makedirs(path_to_json)
    # run jvm2json on file
    jvm2json_command = "jvm2json -s " + file + " -t " + path_to_json + "/" + file_name + ".json"
    jq_command = "cat " + path_to_json + "/" + file_name + ".json" + " | jq '.' > bin/" + project_name + "/JQFiles/" + file_name + ".json"
    subprocess.run(jvm2json_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subprocess.run(jq_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)    

if os.path.exists("graphbyte.dot"):
    os.remove("graphbyte.dot")

f = open("graphbyte.dot", "w")
f.write("digraph G {\n")
filenameArr = []
setup(f)
legend(f)

dependencies = []

def replaceJson(name):
    return name.replace(".json","")

for file_name in os.listdir(path_to_json):
    if(file_name.endswith('.class')):
        continue
    filenameArr.append(file_name.replace('.json', ''))
    print(path_to_json)
    file = open(os.path.join(path_to_json, file_name), 'r',encoding='utf-8',errors='ignore')
    data = json.load(file)
    
    methods = []
    fields = []
    print(file_name)

    # Finds extends relation 
    if ('super' in data and data['super'] != None):
        superclass = data['super']
        super_name = superclass['name'].split('/')[-1]
        if (super_name != 'Object'):
            dependencies.append((file_name, "INHERITANCE", super_name))

    # Finds implements relation
    if ('interfaces' in data and len(data['interfaces']) > 0):
        interfaces = data['interfaces']
        for interface in interfaces:
            interface = interface['name'].split('/')[-1]
            dependencies.append((file_name, "REALIZATION", interface))

    # Finds fields
    json_fields = data['fields']
    for field in json_fields:
        name = field['name']
        if (checkname(name) != "JSONERROR"):
            if(field['access'][0] == 'public'):
                access = '+'
            elif(field['access'] == 'protected'):
                access = '#'
            else:
                access = '-'
            fieldType = getObjectType(field)

            # If field type starts with a capital letter, its an aggregation
            if (fieldType[0].isupper()):
                dependencies.append((file_name, "AGGREGATION", fieldType))

            fields.append(access + name + ':' + fieldType)
        
    # Finds methods
    json_methods = data['methods']
    for method in json_methods:
        name = method['name']
        if (name != '<init>' and name != '<clinit>'): 
            if (method['access'][0] == 'public'):
                access = '+'
            elif(method['access'][0] == 'protected'):
                access = '#'
            else:
                access = '-'
            params_string = getObjectParameters(method)
            returns = method['returns']
            returnType = getObjectType(returns)
            methods.append(access + name + '(' + params_string + ')' + ':' + returnType)
            
    print(methods)
    print(fields, "\n")

    makeGraphNode(f,file_name,methods,fields)

#Composition
for i in range(len(filenameArr)):
    for j in range(len(filenameArr)):
        if i==j:
            continue
        if(str(filenameArr[i]).startswith(str(filenameArr[j]))):
            f.write(str(filenameArr[i]) + "->" + str(filenameArr[j]) + "[arrowhead=odiamond]\n")

print(dependencies)
#Realization

dependencies = list(set(dependencies))
print()
print(methods)
print(fields)
print(dependencies)
for depedency in dependencies:
    dep0 = replaceJson(depedency[0])
    dep2 = replaceJson(depedency[2])
    dep0 = stringReplace(dep0)
    dep2 = stringReplace(dep2)
    if(depedency[1] == "REALIZATION"):
        f.write(dep0 + "->" + str(dep2) + "[arrowhead=dot]\n")
    if(depedency[1] == "INHERITANCE"):
        f.write(str(dep0) + "->" + str(dep2) + "[arrowhead=crow]\n")
    if(depedency[1] == "AGGREGATION"):
        f.write(str(dep0) + "->" + str(dep2) + "[arrowhead=odot]\n")
    if(depedency[1] == "DEPENDENCY"):
        f.write(str(dep0) + "->" + str(dep2) + "[arrowhead=vee]\n")


f.write("}\n")
f.close()
        
