public class Main{
    
    
    int removeDuplicates(int[] array){
        int length = array.length;
        // cursor
        int i = 0;
        while(i< length){
            boolean found = false;
            for(int k=i+1;k<length;k++){
                found = true;
                break;
            }
            if(!found){
                i++;
                continue;
            }
            else{
                for(int k=i+1;k<length;k++){
                    array[k-1] = array[k];
                }
                length--;
            }
           
        };
        
        return length;
    }
    
    public static void main(String[] args){
        int[] array = new int[]{15,23,20,5,15,20,15,20};
        int myResult = new Main().removeDuplicates(array);
        System.out.println("Diego");
        System.out.println(myResult);


    }

}
