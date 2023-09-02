package dtu.gruppe6;


import java.io.File;
import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Runnable { //Calling main main is discouraged

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

			System.out.println(data);

			dependencies = findDependencies(data);

			map.put(file, dependencies);
		}
		try{
			//RemoveDuplicates(map);
			//RemoveSelfDependencies(map);
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
				for(int j = i+1; j<dependencies.size(); j++){
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
		ArrayList<String> dependencies = new ArrayList<>();
        String[] lines = input.split("\\r?\\n");

        Pattern newPattern = Pattern.compile("new\\s+(\\w+)\\s*\\(");
        for (String line : lines) {
            Matcher matcher = newPattern.matcher(line);
            while (matcher.find()) {
                String className = matcher.group(1);
                dependencies.add(className);
            }
        }

		Pattern declarationPattern = Pattern.compile("(new\\s+)?(\\w+)\\s*(?:=|\\(|;)");

        for (String line : lines) {
            Matcher matcher = declarationPattern.matcher(line);
            while (matcher.find()) {
                String className = matcher.group(2);
                if (Character.isUpperCase(className.charAt(0))) {
                    dependencies.add(className);
                }
            }
        }

		return dependencies;
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
		for(String line : lines){
			
			System.out.println(line);
		}

		return imports; 
	}

}
