#include <stdio.h>

//prototypes
void inplace_swap(int *x, int *y);
void reverse_array(int a[], int cnt);
int arraySize(int a[]);
void printArray(int array[], int length);

//--UTILITY
// Gets the size of an int array
int arraySize(int a[]){
    int arrayS = (sizeof(a) / sizeof (a[0]));
    return arrayS;
}

//print contents of the array
void printArray(int array[], int length)
{
    for(int i = 0; i < length; i++){
        printf("%i",array[i]);
    }
}
// An array swapper that doesn't work for odd length arrays
void reverse_array(int a[], int cnt){
    int first, last;
    for(first = 0, last = cnt - 1; first <= last; first++, last--){
        inplace_swap(&a[first], &a[last]);

    }
}
// a simple function to swap values using bit level operations and no third variable required
void inplace_swap(int *x, int *y){
    *y = *x ^ *y; // y is now *x ^ *y
    *x = *x ^ *y; // x is now *x ^ *x ^ *y = y
    *y = *x ^ *y; // y is now *y ^ *y ^ *x = x
}
int main(){
    int r[]= {1, 2, 3, 4, 5};
    int l = arraySize(r);
    printf("%i" , l); //5
    //printArray(r, l);

    return 0;
}