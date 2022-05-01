import java.util.*;
import java.lang.*;
import java.io.*;

public class Code{
static void solve(int a[])

    {

       

    }
    public static void main(String[] args){
        Scanner s = new Scanner(System.in);

        int size = s.nextInt();
        int[] arr = new int[size];

        for(int i = 0;i<size;i++){
            arr[i] = s.nextInt();
        }

        solve(arr);

        for(int i = 0;i<size;i++){
            System.out.print(arr[i] + " ");
        }
        
        s.close();

    }
}