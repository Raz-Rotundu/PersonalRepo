#include <stdio.h>

//prototypes
void inplace_swap(int *x, int *y);
void reverse_array(int a[], int cnt);
int arraySize(int a[]);
void printArray(int array[], int length);
void intMask(int x);

//print contents of the array
void printArray(int array[], int length)
{
    for(int i = 0; i < length; i++){
        printf("%i\n",array[i]);
    }
}
// An array swapper that doesn't work for odd length arrays
void reverse_array(int a[], int cnt){
    int first, last;
    for(first = 0, last = cnt - 1; first < last; first++, last--){
        inplace_swap(&a[first], &a[last]);

    }
}
// a simple function to swap values using bit level operations and no third variable required
void inplace_swap(int *x, int *y){
    *y = *x ^ *y; // y is now *x ^ *y
    *x = *x ^ *y; // x is now *x ^ *x ^ *y = y
    *y = *x ^ *y; // y is now *y ^ *y ^ *x = x
}
//---PART TWO------------------------------------------

// Show the bytes of an object
 typedef unsigned char *byte_pointer;
 
 void show_bytes(byte_pointer start, size_t len) {
   int i;   
   for (i = 0; i < len; i++)
     printf(" %.2x", start[i]);
   printf("\n"); }
 
 void show_int(int x) {
   show_bytes((byte_pointer) &x, sizeof(int));
 }
 
 void show_float(float x) {
   show_bytes((byte_pointer) &x, sizeof(float));
 }

 void show_pointer(void *x) {
   show_bytes((byte_pointer) &x, sizeof(void *));
 }

// A C expression which masks all but the most siginificant byte of int x
void intMask(int x){

    printf("BEFORE: ");
    show_int(x);    //This is a little endian system

    int mask = 0xFF; //mask is FF at the LSB
    printf("MASK: ");
    show_int(mask);

    x = x & mask;

    printf("AFTER: ");
    show_int(x);

}

// A C function which gets the complement of all but the last byte

void compMask(int x){

    printf("BEFORE: ");
    show_int(x);

    int mask = 0x11111100; //Mask is FF at all and 00 at LSB
    printf("MASK: ");
    show_int(mask);

    x = x ^ mask;

    printf("AFTER: ");
    show_int(x);

}
int main(){
    compMask(0x10101022); 




    return 0;
}