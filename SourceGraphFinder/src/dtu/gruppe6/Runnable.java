package dtu.gruppe6;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import dtu.gruppe6.Folders;

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

			

			dependencies = findDependencies(data);

			map.put(file, dependencies);
		}

		printDependencies(map);
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
