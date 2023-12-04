#include <stdio.h>
#include <math.h>


void swap(int *a, int *b);

int main(void)
{
    int x = 1;
    int y = 2;
    int a[3];
    int b[4];
    //fill out the array and print it
    for(int i = 0; i < 4; i++)
    {
        b[i] = i;
        printf("%i ", b[i]);
    }
    printf("\n");
    //reverse the digits
    for (int j = 0; j < (4/2); j++)
    {
        swap(&b[j], &b[3 - j]);
    }
    //print the swapped array
    for(int i = 0; i < 4; i++)
    {
        printf("%i ", b[i]);
    }
    printf("\n");
        //fill out the array and print it
    for(int i = 0; i < 3; i++)
    {
        a[i] = i;
        printf("%i ", a[i]);
    }
    printf("\n");
    //reverse the digits
    for (int j = 0; j < (3/2); j++)
    {
        swap(&a[j], &a[2 - j]);
    }
    //print the swapped array
    for(int i = 0; i < 3; i++)
    {
        printf("%i ", a[i]);
    }
    printf("\n");
    //printf("x is %i, y is %i\n", x, y);
    swap(&x, &y);
    //printf("x is %i, y is %i\n", x, y);
}

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

