#!/bin/bash

 

# Specify the directory containing the .class files
directory="/mnt/c/Users/Tobias Collin/Documents/GitHub/programanalysis/AI-assignments/Classes/student/dtu"

 

# Check if the directory exists
if [ ! -d "$directory" ]; then
  echo "Directory $directory does not exist."
  exit 1
fi

 

# Iterate through all .class files in the directory
for class_file in "$directory"/*.class; do
  # Check if there are any .class files
  if [ -f "$class_file" ]; then
    # Generate the corresponding JSON file name
    json_file="${class_file%.class}.json"

    # Run the jvm2json command
    jvm2json -s "$class_file" -t "$json_file"

    # Check if the command was successful
    if [ $? -eq 0 ]; then
      echo "Converted $class_file to $json_file"
    else
      echo "Error converting $class_file to JSON."
    fi
  fi
done