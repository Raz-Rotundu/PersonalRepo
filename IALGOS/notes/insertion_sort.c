// This would be useful to sort my MTGA hands based on mana cost
#include <stdio.h>


//print contents of the array
void printArray(int array[], int length)
{
    for(int i = 0; i < length; i++){
        printf("%i ",array[i]);
    }
    printf("\n");
}

/*
void insertion_sort(int A[], int len){ 
    for(int i = 1; i <= len; i++){
        int key = A[i];
        // Insert A[i] into sorted subarray A[1: i - 1]
        int j = i - 1;
        while((j > 0) && (A[j] > key)){
            A[j + 1] = A[j];
            j = j - 1;
        }
        A[j + 1] = key;
    }
}
*/

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


}