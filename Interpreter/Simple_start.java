public class Simple_start {
    
    public static void main(String[] args){
        int i = 1; 
        int j;
        j = i + 1;
        System.out.println("Hello World!");
        System.out.println("j = " + j + " i = " + i);
        if(i<j){
            i++;
        }
        else if(i>j){
            i--;
        }
        else{
            i = 0;
        }
        System.out.println("i = " + i);
        System.out.println("j = " + j);
        for(int k = 0; k < 10; k++){
            System.out.println("k = " + k);
        }
        int l = 0;
        while(l < 10){
            l++;
        }
        System.out.println("l = " + l);
        
        
    }
}
