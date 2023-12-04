#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

//experiments with modulo
bool checksum(string numstr);
//checksum functions
int otherSum(long in, int len);
int lastSum(long in, int len);
int main(void)
{

    string number = get_string("Number: ");
    int len = strlen(number);
    long lnumber = atol(number);
    printf("STRING: %s\n", number);
    printf("LONG: %li\n", lnumber);
    printf("LENGTH: %i\n", len);
    //bool valid = IsVisa(number);
    //1= true, 0 = false
    bool check = checksum(number);
    printf("%i\n", check);

}
bool checksum(string numstr)
{
    //length of num
    int length = strlen(numstr);
    //convert to long
    long longNum = atol(numstr);
    int total = otherSum(longNum, length) + lastSum(longNum, length);
    if(total%10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

int otherSum (long in, int len)
{
     //exponent for finding every other number
    int x = 2;
    int sum = 0;
    //selects every other integer, starting from second last
    for(int i = 0; i < len; i++)
    {
        long pwr = pow(10, x);
        long div = pow(10, x-1);
        long current = ((in%pwr)/div);
        //digit is multiplied by two
        current = current * 2;
        //the result is then broken into individual digits, and added together
        for(int z = 1; z < 3; z++)
        {
            long subpwr = pow(10,z);
            long subdiv = pow (10, z-1);
            long subcurrent = ((current%subpwr)/subdiv);
            sum = sum + subcurrent;
            //printf("Adding: %li\n", subcurrent);

        }
        //printf("SUM: %i\n", sum);
        x = x + 2;
    }
    return sum;

}
int lastSum(long in, int len)
{
     //exponent for finding every other number
    int x = 1;
    int sum = 0;
    //selects every other integer, starting from last
    for(int i = 0; i < len; i++)
    {
        long pwr = pow(10, x);
        long div = pow(10, x-1);
        long current = ((in%pwr)/div);
        //result is summed together
        sum = sum + current;
       // printf("CURRENT: %li\n", current);
       // printf("SUM: %i\n", sum);
        x = x + 2;
    }
    return sum;
}
    /*long number = 1234;
    printf("%li\n", number % 1); //10^0
    printf("%li\n", number % 10); //10^1
    printf("%li\n", number % 100); // 10^2
    printf("%li\n", number % 1000); //10^3
    printf("%li\n", number % 10000); //10^4*/

    /*single digit separation
    /printf("%li\n", (number % 10)/1); //10^1
    printf("%li\n", (number % 100)/10); // 10^2
    printf("%li\n", (number % 1000)/100); //10^3
    printf("%li\n", (number % 10000)/1000); //10^4*/




