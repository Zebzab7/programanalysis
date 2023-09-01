package dtu.gruppe6;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class Runnable { //Calling main main is discouraged

	public static void main(String[] args) throws IOException{
		String workingDirectory = System.getProperty("user.dir");
		String Path = workingDirectory + "/course-02242-examples-main"; //Starting path
		ArrayList<File> subfolders = new ArrayList<File>();
		ArrayList<File> allfolders = new ArrayList<File>();
		ArrayList<File> files = new ArrayList<File>();
		ArrayList<FileAtrribute> fileInfo = new ArrayList<>();
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
						String keyword = file.getName();
						keyword = keyword.replace(".java", "");
						Runnable outer = new Runnable();
						Runnable.FileAtrribute fa = outer.new FileAtrribute(keyword,file.getPath());
						fileInfo.add(fa);
					}
				}
			}
		}
		//Prints all files
		PrintFileFolder(files);
		System.out.println("Files found: " + files.size());

		//prints all the dependencies
		ArrayList<ArrayList<String>> de = FindDenpendencies(fileInfo);
		for (ArrayList<String> arrayList : de) {
			if (arrayList.size()==1) {
				System.out.println("There is no dependency in "+arrayList.get(0));
			}else{
				System.out.print(arrayList.get(0)+"'s dependencies is ");
				for (int i=1;i< arrayList.size();i++) {
					if (i<arrayList.size()-1) {
						System.out.print(arrayList.get(i)+",");
					}else{
						System.out.println(arrayList.get(i)+";");
					}
					
				}
			}
			
		}

		
		// String data;
		// data = getFileData(files.get(0));
		// //remove commented lines
			
		// System.out.println(data);


	}
	//find all the dependencies in files
	public static ArrayList<ArrayList<String>> FindDenpendencies(ArrayList<FileAtrribute> fileInfo) throws IOException{

		ArrayList<ArrayList<String>> dependencies = new ArrayList<>();
		for (FileAtrribute fa: fileInfo) {
			ArrayList<String> s = new ArrayList<>();
			s.add(fa.fileName);
			FileInputStream inputStream = new FileInputStream(fa.filePath);
			BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
			String line;
			String keyword,str;
			while((line = bufferedReader.readLine())!=null){
				line = line.replaceAll("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)","")
				   .replaceAll("(?m)^\\s*$", "");
				if (line.contains("import")  ) {
					str = line.substring(0, line.indexOf(" "));
					keyword = line.substring(str.length()+1, line.length()-1);
					s.add(keyword);
				}
				
			}
			dependencies.add(s);
		}
		return dependencies;
		
	}
    

	// public static String getFileData(File file){
	// 	try {
	// 		String content = Files.readString(file.toPath());
	// 		return content;
	// 	} catch (IOException e) {
	// 		e.printStackTrace();
	// 	}
	// 	return null;
	// }


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

	
	public class FileAtrribute{
		String fileName;
		String filePath;
		public FileAtrribute(String fileName, String filePath) {
			this.fileName = fileName;
			this.filePath = filePath;
		}
		public String getFileName() {
			return fileName;
		}
		public void setFileName(String fileName) {
			this.fileName = fileName;
		}
		public String getFilePath() {
			return filePath;
		}
		public void setFilePath(String filePath) {
			this.filePath = filePath;
		}
		
	}
}


