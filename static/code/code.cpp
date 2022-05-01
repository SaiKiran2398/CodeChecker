#include<bits/stdc++.h>

using namespace std;

void solve(int a[], int arr_size)

{

    int lo = 0;

    int hi = arr_size - 1;

    int mid = 0;

 

    // Iterate till all the elements

    // are sorted

    while (mid <= hi) {

        switch (a[mid]) {

 

        // If the element is 0

        case 0:

            swap(a[lo++], a[mid++]);

            break;

 

        // If the element is 1 .

        case 1:

            mid++;

            bre

 

        // If the element is 2

        case 2:

            swap(a[mid], a[hi--]);

            break;

        }

    }

}
int main(){
    
    int size;
    cin>>size;
    int * arr = new int[size];

    for(int i = 0;i<size;i++){
        cin>>arr[i];
    }

    solve(arr,size);

    for(int i = 0;i<size;i++){
        cout<<arr[i]<<" ";
    }

}