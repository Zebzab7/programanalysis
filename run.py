from tree_sitter import Language, Parser
import os
import re

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
    
    def find_subtree_node(self, root_node_tree, type):
        if not root_node_tree:
            return None
        if root_node_tree.type == type:
            return root_node_tree
        for child in root_node_tree.children:
            node = self.find_subtree_node(child, type)
            if node:
                return node
            
    def traverse(self, node):
        if not node:
            return None
        print(node.type)
        print(f'{node.text}')
        for child in node.children:
            self.traverse(child)

folder_path = 'course-02242-examples-main/course-02242-examples-main'
# Create an instance of SyntaxFold
Sf = SyntaxFold()
# Call the function using the instance
Sf.visitFiles(folder_path)

# for i in range(len(syntaxString)):
#     print("File is:", files[i])
#     Sf.printTree(syntaxString[i])

for i in range(len(trees)):
    print("File is:", files[i])
    Sf.traverse(Sf.find_subtree_node(trees[i],"package_declaration"))
    print("\n")