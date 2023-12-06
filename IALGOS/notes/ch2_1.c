// This would be useful to sort my MTGA hands based on mana cost
#include <stdio.h>
#include <stdbool.h>


//print contents of the array
void printArray(int array[], int length)
{
    for(int i = 0; i < length; i++){
        printf("%i ",array[i]);
    }
    printf("\n");
}

//Linear search for a value in an array
bool linear_search(int a[], int len, int val){
    for(int i = 0; i < len; i++){
        if(a[i] == val){
            return true;
        }
    }
    return false;
}

// Adds bits in an array representation of bit vector. Assumes only 1 and 0s on arrays of same size!
void bin_add(int a[], int b[], int len){
    int carry = 0;

    int c[len];

    for(int i = (len -1); i >= 0; i--){
        int sum = a[i] + b[i] + carry;
        if(sum > 1){
            carry = 1;
            c[i] = 0;
        }
        else{
            carry = 0;
            c[i] = sum;
        }
    }
    printArray(c, len);
}
// Insertion sort into an array
void insertion_sort(int A[], int len){
    for(int i = 1; i < len; i++){
        int key = A[i];
        int j = i - 1;
        while((j >= 0) && (A[j] > key)){
            A[j + 1] = A[j];
            j = j - 1;
        }
        A[j + 1] = key;

    }
}
int main(){
    

    int arrayA[] = {0, 1, 1, 0};
    int arrayB[] = {1, 0, 0, 1};
    int arrayC[] = {0, 0, 1, 0};
    bin_add(arrayA, arrayB, 4); //1111
    bin_add(arrayA, arrayC, 4); //1000
    /*
    // The array to be sorted
    int array[] = {99, 9, 5, 7, 1};

    // The length of the array
    int len = sizeof(array) / sizeof(array[0]);

    
    // Print array as is 
    printf("BEFORE:----------------\n");
    printArray(array, len);

    // Sort and display new array
    insertion_sort(array, len);
    printf("AFTER--------------\n");
    printArray(array, len);
    */

   /*   printf("%d\n", linear_search(array, len, 8)); //F
   printf("%d\n", linear_search(array, len, 9)); //T
   */



}