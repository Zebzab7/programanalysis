from tree_sitter import Language, Parser
FILE = "./languages.so" # the ./ is important
Language.build_library(FILE, ["tree-sitter-java"])
JAVA_LANGUAGE = Language(FILE, "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)
with open("/home/shreyassgs00/Desktop/program_analysis/repo_stuff/programanalysis/course-02242-examples-main/course-02242-examples-main/src/dependencies/java/dtu/deps/normal/Primes.java", "rb") as f:
    tree = parser.parse(f.read())
# the tree is now ready for analysing
print(tree.root_node.sexp())