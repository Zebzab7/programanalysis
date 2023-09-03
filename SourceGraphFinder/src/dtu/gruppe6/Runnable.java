package dtu.gruppe6;


import java.io.File;
import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class RunnableMaster { //Calling main main is discouraged

	public static void main(String[] args) {
		String workingDirectory = System.getProperty("user.dir");
		String Path = workingDirectory + "/course-02242-examples-main"; //Starting path
		
		ArrayList<File> files = new ArrayList<File>();

		HashMap<File, ArrayList<String>> map = new HashMap<>();
		
		files = Folders.findFiles(Path);
	
		String data = null;
		ArrayList<String> dependencies = new ArrayList<String>();
		for (int i = 0; i < files.size(); i++) {
			File file = files.get(i);

			data = getFileData(file);
			//remove commented lines
			data = data.replaceAll("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)","")
					   .replaceAll("(?m)^\\s*$", "");
			data = removeClass(data);

			// System.out.println(data);

			dependencies = findDependencies(data);

			map.put(file, dependencies);
		}
		try{
			RemoveDuplicates(map);
			RemoveSelfDependencies(map);
			makeGraph(map);
		}catch(IOException e){
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
		
		printDependencies(map);
	}
	public static void RemoveDuplicates(HashMap<File, ArrayList<String>> map){
		for(File file : map.keySet()){
			ArrayList<String> dependencies = map.get(file);
			for(int i = 0; i<dependencies.size(); i++){
				for(int j = 0; j<dependencies.size(); j++){
					if(i == j){
						continue;
					}
					if(dependencies.get(i).equals(dependencies.get(j))){
						dependencies.remove(j);
					}
				}
			}
		}
	}
	public static void RemoveSelfDependencies(HashMap<File, ArrayList<String>> map){
		for(File file : map.keySet()){
			ArrayList<String> dependencies = map.get(file);
			
			for(int i = 0; i<dependencies.size(); i++){
				if(dependencies.get(i).equals(file.getName().replace(".java", ""))){
					dependencies.remove(i);
				}
			}
		}
	}

	public static void makeGraph(HashMap<File, ArrayList<String>> map) throws IOException {
		//Makes file and removes if exists
		File myObj = new File("graph.dot");
		if(myObj.createNewFile()){
				System.out.println("File created: " + myObj.getName());
		}else{
			myObj.delete();
			myObj.createNewFile();
		}
		
		ArrayList<String> dependencies = new ArrayList<String>();
		String start = "digraph G {\n";
		Path fileName = Path.of("graph.dot");

		Files.writeString(fileName, start);
		//Foreach file in map find dependencies and write to file
		for(File file: map.keySet()){
			dependencies = map.get(file);
			for(String dependency: dependencies){
				String line = file.getName();
				line = line.replace(".java", "");
				line += " -> " + dependency + "\n";
				Files.writeString(fileName, line, java.nio.file.StandardOpenOption.APPEND);
			}
		}
		Files.writeString(fileName, "}", java.nio.file.StandardOpenOption.APPEND);
	}

	public static void printDependencies(HashMap<File, ArrayList<String>> map) {
		for (File file : map.keySet()) {
			System.out.println(file.getName() + ":");
			for (String dependency : map.get(file)) {
				System.out.println("-> " + dependency);
			}
			System.out.println();
		}
	}
		
	public static ArrayList<String> findDependencies(String data) {
		ArrayList<String> dependencies = new ArrayList<String>();

		dependencies.addAll(getImports(data));
		dependencies.addAll(findOtherDependencies(data));

		return dependencies;
	}

	/**
	 * Find dependencies other beside imports
	 * @param input
	 * @return
	 */
	public static ArrayList<String> findOtherDependencies(String input) {

		HashSet<String> dependencies = new HashSet<>();
		ArrayList<Pattern> patterns = new ArrayList<Pattern>();

		// Matches declared objects
		final String declaredObjectRegex = "([A-Z][a-z]*)(?=\\s([A-Za-z]*);)";
		final Pattern declaredObjectPattern = Pattern.compile(declaredObjectRegex, Pattern.MULTILINE);
		patterns.add(declaredObjectPattern);

		// Matches initialized objects
		final String newObjectRegex = "(?<=new\\s)([A-Z][a-z]*)";
		final Pattern newObjectPattern = Pattern.compile(newObjectRegex, Pattern.MULTILINE);
		patterns.add(newObjectPattern);

		// Matches method calls
		final String methodCallRegex = "([A-Z][a-z]*)(?=(\\.([A-Za-z]*))+\\()";
		final Pattern methodCallPattern = Pattern.compile(methodCallRegex, Pattern.MULTILINE);
		patterns.add(methodCallPattern);

		// Matches method calls with parameters and declarations with commas (e.g. "String a, b, c")
		final String methodCallWithParametersRegex = "([A-Za-z]*)(?=(\\[\\])?\\s+([A-Za-z]*)(\\)|\\s*\\,))";
		final Pattern methodCallWithParametersPattern = Pattern.compile(methodCallWithParametersRegex, Pattern.MULTILINE);
		patterns.add(methodCallWithParametersPattern);

		// Matches return types in function headers
		final String returnTypeRegex = "((?<=public\\s)|(?<=private\\s)|(?<=public static\\s)|(?<=private\\sstatic\\s))(void|[A-Z][a-z]*)";
        final Pattern returnTypePattern = Pattern.compile(returnTypeRegex, Pattern.MULTILINE);
		patterns.add(returnTypePattern);

		//Matches the inner class in the outer class 
		//eg:Runnable.FileAtrribute fa = outer.new FileAtrribute(keyword,file.getPath());
		final String innerClassRegx = "^\\s*(\\w+\\.\\w+)\\s+(\\w+)\\s*=\\s+(\\w+)\\.new\\s+(\\w+)\\(([^)]*)\\)"; 
		final Pattern innerClassPatter = Pattern.compile(innerClassRegx, Pattern.MULTILINE);
		patterns.add(innerClassPatter);

		for (Pattern pattern : patterns) {
			final Matcher matcher = pattern.matcher(input);
			while (matcher.find()) {
				// for (int i = 1; i <= matcher.groupCount(); i++) {
				// 	System.out.println("Group " + i + ": " + matcher.group(i));
				// }
				dependencies.add(matcher.group(0));
			}
		}

		// Remove empty strings and void
		if (dependencies.contains("")) {
			dependencies.remove("");
		}
		if (dependencies.contains("void")) {
			dependencies.remove("void");
		}

		return new ArrayList<>(dependencies);
	}
	
	public static String getFileData(File file){
		try {
			String content = Files.readString(file.toPath());
			return content;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}

	public static String removeClass(String data){
		String[] lines = data.split("\n");
		for(String line : lines){
			if(line.startsWith("public class")||line.startsWith("private class")||line.startsWith("protected class")||line.startsWith("class")){
				data = data.replace(line, "");

			}
		}
		return data;
	}

	public static ArrayList<String> getImports(String File){
		ArrayList<String> imports = new ArrayList<String>();
		String[] lines = File.split("\n");
		for(String line : lines){
			if(line.startsWith("import")){
				if(line.endsWith(".*;")){
					line = line.replace(".*;", "");
				}
				line = line.replace("import ", "");
				line = line.replace(";", "");
				for(int i = 0; i<imports.size(); i++){
					if(imports.get(i).equals(line)){
						break;
					}else{
						imports.add(line);
					}
				}
			}
		}

		return imports; 
	}

}
