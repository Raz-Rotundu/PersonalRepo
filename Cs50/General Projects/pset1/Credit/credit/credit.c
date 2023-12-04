#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

//Raz Rotundu 2022

//Verify first two and number length
bool IsAmex(string numstr);
bool IsMaster(string numstr);
bool IsVisa(string numstr);

//do the checksum operation
bool checksum(string numstr);
//checksum functions
int otherSum(long in, int len);
int lastSum(long in, int len);

int main(void)
{
    //get user input as string(for determining length)
    string numberString = get_string("Number: ");
    //card type
    string CardType;
    //verify card type
    //bool validity = IsAmex(numberString);
    if (IsAmex(numberString) == true)
    {
        CardType = "AMEX";
        if (checksum(numberString) != true)
        {
            CardType = "INVALID";
        }
    }
    else if (IsMaster(numberString) == true)
    {
        CardType = "MASTERCARD";
        if (checksum(numberString) != true)
        {
            CardType = "INVALID";
        }
    }
    else if (IsVisa(numberString) == true)
    {
        CardType = "VISA";
        if (checksum(numberString) != true)
        {
            CardType = "INVALID";
        }
    }
    else
    {
        CardType = "INVALID";
    }
    printf("Number: %s\n", CardType);
}

//AMEX definition
bool IsAmex(string numstr)
{
    int length = strlen(numstr);
    long number = atol(numstr);
    //check the lenght first
    if (length == 15)
    {
        //checks the last two digits next
        long PowTen = pow(10, length);
        long divisor = pow(10, (length - 2));
        //modulo for the last two digitd
        long LastTwo = ((number % PowTen) / divisor);
        if (LastTwo == 34 || LastTwo == 37)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    else
    {
        return false;
    }
    //return false by default
    return false;
}
//MASTER definition
bool IsMaster(string numstr)
{
    int length = strlen(numstr);
    long number = atol(numstr);
    //check the lenght first
    if (length == 16)
    {
        //checks the last two digits next
        long PowTen = pow(10, length);
        long divisor = pow(10, (length - 2));
        //modulo for the last two digitd
        long LastTwo = ((number % PowTen) / divisor);
        if (LastTwo == 51 || LastTwo == 52 || LastTwo == 53 || LastTwo == 54 || LastTwo == 55)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    else
    {
        return false;
    }
    //return false by default
    return false;
}
//VISA Definition
bool IsVisa(string numstr)
{
    int length = strlen(numstr);
    long number = atol(numstr);
    //check the lenght first
    if (length == 13 || length == 16)
    {
        //checks the last two digits next
        long PowTen = pow(10, length);
        long divisor = pow(10, (length - 1));
        //modulo for the last two digitd
        long LastOne = ((number % PowTen) / divisor);
        if (LastOne == 4)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    else
    {
        return false;
    }
    //return false by default
    return false;
}
bool checksum(string numstr)
{
    //length of num
    int length = strlen(numstr);
    //convert to long
    long longNum = atol(numstr);
    int total = otherSum(longNum, length) + lastSum(longNum, length);
    if (total % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

int otherSum(long in, int len)
{
    //exponent for finding every other number
    int x = 2;
    int sum = 0;
    //selects every other integer, starting from second last
    for (int i = 0; i < len; i++)
    {
        long pwr = pow(10, x);
        long div = pow(10, x - 1);
        long current = ((in % pwr) / div);
        //digit is multiplied by two
        current = current * 2;
        //the result is then broken into individual digits, and added together
        for (int z = 1; z < 3; z++)
        {
            long subpwr = pow(10, z);
            long subdiv = pow(10, z - 1);
            long subcurrent = ((current % subpwr) / subdiv);
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
    for (int i = 0; i < len; i++)
    {
        long pwr = pow(10, x);
        long div = pow(10, x - 1);
        long current = ((in % pwr) / div);
        //result is summed together
        sum = sum + current;
        // printf("CURRENT: %li\n", current);
        // printf("SUM: %i\n", sum);
        x = x + 2;
    }
    return sum;
}