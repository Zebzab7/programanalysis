package dtu.gruppe6;

import java.io.File;
import java.util.ArrayList;

public class Folders {
    
    public static ArrayList<File> findFiles(String Path){
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
		}


        return files;
    }
    private static ArrayList<File> findSubFolders(ArrayList<File> subfolders) {
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
