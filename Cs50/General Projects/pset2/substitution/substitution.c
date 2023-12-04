#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Raz Rotundu 2022

//prototypes
string encode(string plain, string key);
bool doublecheck(string in);

int main(int argc, string argv[])
{
    //check for correct key format
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    //check for correct key length
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    //check that key is alphabetical
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isalpha(argv[1][i]))
        {
            //not alphabetical
            return 1;
        }
    }
    //check that there are no duplicates
    if (!doublecheck(argv[1]))
    {
        //repeated characters in key
        return 1;
    }
    string plaintext = get_string("Plaintext: ");
    printf("ciphertext: %s\n", encode(plaintext, argv[1]));

}
//encodes plaintext based on key
string encode(string plain, string key)
{
    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string cipher;
    //go through each character of the plaintext
    for (int i = 0; i < strlen(plain); i++)
    {
        //if it's a letter
        if (isalpha(plain[i]))
        {
            //and it's uppercase
            if (isupper(plain[i]))
            {
                //iterate through the ALPHABET
                for (int j = 0; j < strlen(ALPHABET); j++)
                {
                    //if match found
                    if (ALPHABET[j] == plain[i])
                    {
                        //translate into equivalent key position, retain capitalization
                        plain[i] = toupper(key[j]);
                        break;
                    }
                }
            }
            //else it's lowercase
            else
            {
                //iterate through the alphabet
                for (int j = 0; j < strlen(alphabet); j++)
                {
                    //if match found
                    if (alphabet[j] == plain[i])
                    {
                        //translate into equivalent key position, retain capitalization
                        plain[i] = tolower(key[j]);
                        break;
                    }
                }
            }
        }
    }
    cipher = plain;
    return cipher;
}

//checks strings for repeated characters, returns true if all unique
bool doublecheck(string in)
{
    //26 blank spaces
    char prev[26];
    //iterate over every char of the input
    for (int i = 0; i < strlen(in); i++)
    {
        //check it against every char of the prev characters
        for (int j = 0; j < strlen(prev); j++)
        {
            //if repetition is found, return false, make equal capitalization
            if (tolower(in[i]) == tolower(prev[j]))
            {
                return false;
            }
        }
        //otherwise add it to the prev character string
        prev[i] = in[i];
    }
    //return true if unique
    return true;
}