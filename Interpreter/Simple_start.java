public class Simple_start {
    public static int i, j; 
    
    public static void main(String[] args){
        int z = 10;
        i = 1;
        j = i + 1 + z;
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

    @Case
    public boolean multiply(int value, int multiplier){
        return value * multiplier;
    }
}
