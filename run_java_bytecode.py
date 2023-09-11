import json
import os

directory = os.path.dirname(__file__)
relative_path = "AI-assignments/Classes/student/dtu"
full_path = os.path.join(directory, relative_path)

for file_name in os.listdir(full_path):
    if file_name.endswith('.json'):
        file = open(os.path.join(full_path, file_name), 'r')
        data = json.load(file)
        for i in data:
            print(i)
            break
        