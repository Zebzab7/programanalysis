import json
import os

directory = os.path.dirname(__file__)
relative_path = "AI-assignments/Classes/student/dtu"
full_path = os.path.join(directory, relative_path)

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
  