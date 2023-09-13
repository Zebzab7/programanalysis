from tree_sitter import Language, Parser
import os
import re
import json

# with open("java-tree-sitter/src/test/java/ai/serenade/treesitter/ParserTest.java", "rb") as f:
#     tree = parser.parse(f.read())
# # the tree is now ready for analysing
# print(tree.root_node.sexp())

## read folds and files and make them into
syntaxString = []
files =[]
trees = []
class SyntaxFold:
    def delcomments(self,content):
        # Remove single-line comments
        content = re.sub(r'//.*', '', content)     
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content
    
    def remove_empty_lines(self,content):
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        result_content = '\n'.join(non_empty_lines)
        return result_content
     
    def visitFiles(self,path):
        # List all files in the folder
        file_list = os.listdir(path)    
        # Loop through the files and read them
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            # Check if it's a file (not a subfolder)
            if file_name.lower().endswith(".java"):
                files.append(file_name)
                with open(file_path,"r") as file:
                    content = self.delcomments(file.read())
                    final_content = self.remove_empty_lines(content)
                    contentTree, class_tree = self.syntaxFiles(final_content)
                    syntaxString.append(contentTree)
                    trees.append(class_tree)
            elif os.path.isfile(file_path)==False:
                self.visitFiles(file_path)
                    # self.syntaxFiles(file_name, content)
            else:
                continue  
                     
               
    def syntaxFiles(self,content):
        # Using str.encode() method to convert a string to bytes
        byte_content = bytes(content,'utf-8')
        FILE = "./languages.so" # the ./ is important
        Language.build_library(FILE, ["tree-sitter-java"])
        JAVA_LANGUAGE = Language(FILE, "java")
        parser = Parser()
        parser.set_language(JAVA_LANGUAGE)      
        tree = parser.parse(byte_content)
        return tree.root_node.sexp(), tree.root_node
    
    def printTree(self,string):
        i=0
        splitString = string.split("(")
        
        for i in range(len(splitString)):
            add = ""

            add += "("
            print(add + splitString[i])
        for i in range(3):
            print(" ")
            
        return
    

    def find_subtree_node_and_append_to_list(self, root, type, nodes):
        if not root:
            return None
        if root.type == type:
            nodes.append(root)
        for child in root.children:
            self.find_subtree_node_and_append_to_list(child, type, nodes)

    def find_subtree_node(self, root, type):
        if not root:
            return None
        if root.type == type:
            return root
        for child in root.children:
            type_node = self.find_subtree_node(child, type)
            if type_node:
                return type_node
            
    def traverse(self, node):
        if not node:
            return None
        print(node.type+'\t'+f'{node.text}')
        #print(f'{node.text}')
        for child in node.children:
            self.traverse(child)
    
    def legend(self,f):
        f.write("subgraph cluster {\n")
        f.write("j->k[label=\" dependency\",arrowhead=vee]\n")
        f.write("g->h[label=\" composition\",arrowhead=odiamond]\n")
        f.write("e->f[label=\" aggregation\",arrowhead=odot]\n")
        f.write("c->d[label=\" realization\",arrowhead=dot]\n")
        f.write("a->b[label=\" inheritance\",arrowhead=crow]\n")
        f.write("}\n")
    
    def setup(self,f):
        f.write("node [shape=record style=filled fillcolor = gray95]\n")
        f.write("edge [fontname=\"Helvetica,Arial,sans-serif\"]\n")

    def stringReplace(self,i):
        i=i.replace("b'","")
        i=i.replace("'","")
        i=i.replace("<","_")
        i=i.replace(">","")
        return i

    def makeGraph(self,lists,files):
        if os.path.exists("graph.dot"):
            os.remove("graph.dot")
        # Create a new file
        f = open("graph.dot", "a")

        #legend
        f.write("digraph G {\n")
        self.setup(f)
        self.legend(f)
        print(lists)
        for i in range(len(lists)):
            importDeclarations = []
            #Write name of file
            filename =files[i]
            filename = filename.replace(".java","")
            

            fieldDeclaration = lists[i]["field_declaration"]
            classDeclarations = lists[i]["class_declaration"]
            #gets imports
            for j in range(len(lists[i]["import_declaration"])):
                if lists[i]["import_declaration"][j] not in importDeclarations:
                    importDeclarations.append(lists[i]["import_declaration"][j])

            #gets class declarations
            realizations = []
            inheritances = []
            compositions = []
            fields = []
            imports = []
            for j in range(len(classDeclarations)):
                
                if classDeclarations[j][1] == "REALIZATION":
                    if classDeclarations[j][0] not in realizations:
                        realizations.append(classDeclarations[j][0])
                elif classDeclarations[j][1] == "INHERITANCE":
                    if classDeclarations[j][0] not in inheritances:
                        inheritances.append(classDeclarations[j][0])
                elif classDeclarations[j][1] == "COMPOSITION":
                    if classDeclarations[j][0] not in compositions:
                        compositions.append(classDeclarations[j][0])
            for j in range(len(fieldDeclaration)):
                if fieldDeclaration[j][1] == "FIELD":
                    if fieldDeclaration[j][0] not in compositions:
                        fields.append(fieldDeclaration[j][0])
            for j in range(len(importDeclarations)):
                imports.append(importDeclarations[j])
            
                
            f.write(filename + "[label = <{<b>"+filename+"</b> |")
            for i in range(len(fields)):
                i=self.stringReplace(fields[i])
                f.write("+ "+i+"<br align=\"left\"/>")
            f.write("|")
            f.write("+ methods()<br align=\"left\"/>")
            f.write("}>]\n")
            for i in realizations:
                i=self.stringReplace(i)
                f.write(i + "->" + filename + "[arrowhead=dot]\n")
            for i in inheritances:
                i=self.stringReplace(i)                
                f.write(i + "->" + filename + "[arrowhead=crow]\n")
            for i in compositions:
                i=self.stringReplace(i)
                f.write(i + "->" + filename + "[arrowhead=odiamond]\n")
            for i in imports: 
                i=self.stringReplace(i)
                i=i.replace(".","_")
                i=i.replace("*","")
                f.write(i + "->" + filename + "[arrowhead=vee]\n")
        # Write the graph in the file
        #FileName()[label = <{<b>«FileName()</b> | + FieldName()<br align="left"/>FieldName()<br align="left"/>|+ functionName()<br align="left"/>functionName()<br align="left"/>}>]


        # Needs more code
        #if("inheritance")
            #f.write("arrowhead=crow]")
        #if("relization")
            #f.write("arrowhead=dot]")
        #if("aggregation")
            #f.write("[arrowhead=odot]")
        #if("composition")
            #f.write("[arrowhead=odiamond]")
        #if("dependency")
            #f.write("[arrowhead=vee]")
        
        f.write("}") #End of file
        f.close()

    def find_inner_classes(class_node):
        inner_classes = []

        Sf.find_subtree_node_and_append_to_list(class_node, "class_declaration", inner_classes)
        return inner_classes

def readAST():
    folder_path = 'course-02242-examples-main/course-02242-examples-main'
    # Create an instance of SyntaxFold
    Sf = SyntaxFold()
    # Call the function using the instance
    Sf.visitFiles(folder_path)

    for i in range(len(trees)):
        print("File is:", files[i])
        if (i == 2):
            Sf.traverse(trees[i])

        subnode_types = ["import_declaration", "package_declaration", "class_declaration", "field_declaration"]

        # Create len(files) dictionaries
        file_dictionaries = []

        # Initialize and populate the dictionaries
        for i in range(len(files)):  
            dictionary = {}
    
            for subnode_type in subnode_types:
                if subnode_type == "import_declaration":
                    nodes = []
                    Sf.find_subtree_node_and_append_to_list(trees[i],subnode_type, nodes)

                    node_texts = []
                    for node in nodes:
                        text = str(node.text)
                        text = text.split(" ")[1]

                        pattern = r'([^;]+);'
                        match = re.search(pattern, text)

                        if match:
                            result = match.group(1)
                            node_texts.append((result, "DEPENDENCY"))

                    # Initialize the key-value pair
                    dictionary[subnode_type] = node_texts
                
                if subnode_type == "class_declaration":
                    nodes = []
                    Sf.find_subtree_node_and_append_to_list(trees[i], subnode_type, nodes)
                    list_of_matches = []
                    
                    for node in nodes:
                        # Extract class name
                        super_interfaces = Sf.find_subtree_node(node, "super_interfaces")
                        if super_interfaces:
                            generic_type = str(Sf.find_subtree_node(node, "type_list").text)
                            list_of_matches.append((generic_type, "REALIZATION"))

                        super_class = Sf.find_subtree_node(node, "superclass")
                        if super_class:
                            identifier = str(Sf.find_subtree_node(super_class, "type_identifier").text)
                            list_of_matches.append((identifier, "INHERITANCE"))
                        
                        inner_classes = []
                        Sf.find_subtree_node_and_append_to_list(node, "class_declaration", inner_classes)
                        inner_classes.pop(0)
                        if inner_classes:
                            for inner_class in inner_classes:
                                identifier = str(Sf.find_subtree_node(inner_class, "identifier").text)
                                list_of_matches.append((identifier, "COMPOSITION"))
                    dictionary[subnode_type] = list_of_matches

                elif subnode_type == "field_declaration":
                    nodes = []
                    Sf.find_subtree_node_and_append_to_list(trees[i], subnode_type, nodes)
                    list_of_matches = []

                    for node in nodes:
                        field = Sf.find_subtree_node(node, "field_declaration")
                        if field:
                            identifier = str(Sf.find_subtree_node(field, "identifier").text)
                            list_of_matches.append((identifier, "FIELD"))

                    dictionary[subnode_type] = list_of_matches

            # Add more key-value pairs as needed
            file_dictionaries.append(dictionary)

        # For each node, traverse the tree
        # for node in nodes:
        #     Sf.traverse(trees[0])

        # print("\n")

    #Print each dictionary in the dictionary list with a newline in between
    for dictionary in file_dictionaries:
        print(dictionary)
        print("\n")

    Sf.makeGraph(file_dictionaries,files)

# n = Sf.find_subtree_node(trees[3],"class_declaration")
# s = Sf.find_subtree_node(n,"super_interfaces")
# print(s.text)
# file = re.sub(r'//.*', '', content) 
