package dtu.gruppe6;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Runnable { //Calling main main is discouraged

	public static void main(String[] args) {
		String workingDirectory = System.getProperty("user.dir");
		String Path = workingDirectory + "/course-02242-examples-main"; //Starting path
		ArrayList<File> subfolders = new ArrayList<File>();
		ArrayList<File> allfolders = new ArrayList<File>();
		ArrayList<File> files = new ArrayList<File>();
		allfolders.add(new File(Path));
		subfolders.add(new File(Path));

		//Finds all subfolders
		while(findSubFolders(subfolders) != null) {
			subfolders = findSubFolders(subfolders);
				for(File folder : subfolders) {
					allfolders.add(folder);
				}
		}

		//Prints all folders found
		//PrintFileFolder(allfolders);

		//Finds all files in all folders
		for(File folder : allfolders) {
			File[] localFiles = new File(folder.getPath()).listFiles(File::isFile);
			if(localFiles != null) {
				for(File file : localFiles) {
					//Finds all java files
					if(file.getName().endsWith(".java")) {
						files.add(file);
					}
				}
			}
			// ?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)
			// notCapture /* notCapture not *

			//Prints all files
			PrintFileFolder(files);
			System.out.println("Files found: " + files.size());
			String data;
			ArrayList<String> imports = new ArrayList<String>();

			data = getFileData(files.get(0));
			//remove commented lines
			data = data.replaceAll("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)","")
				   .replaceAll("(?m)^\\s*$", "");
			System.out.println(findOtherDependencies(data).toString());
			imports = getImports(data);
			data = RemoveClass(data);
			System.out.println(data);
			for(String imp : imports){
				System.out.println(imp);
			}
	}

	/**
	 * Find dependencies other beside imports
	 * @param input
	 * @return
	 */
	public static ArrayList<String> findOtherDependencies(String input) {
		ArrayList<String> dependencies = new ArrayList<>();
        String[] lines = input.split("\\r?\\n");

        Pattern pattern = Pattern.compile("new\\s+(\\w+)\\s*\\(");

        for (String line : lines) {
            Matcher matcher = pattern.matcher(line);
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

	public static String RemoveClass(String data){
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
				imports.add(line);

			}
		}
		return imports; 
	}

	public static ArrayList<File> findSubFolders(ArrayList<File> subfolders) {
		if(subfolders.size() == 0) {
			return null;
		}
		ArrayList<File> folders = new ArrayList<File>();
		for(File folder : subfolders) {
			File[] subfolder = folder.listFiles(File::isDirectory);
			for (File file : subfolder) {
				folders.add(file);
			}
		}
		return folders;
	}
	//Prints files and folders for ease of use
	public static void PrintFileFolder(ArrayList<File> files) {
		for(File file : files){
			System.out.println(file.getPath());
		}
	}

}
