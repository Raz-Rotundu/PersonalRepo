#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

//prototypes
int letterCount(string in);
int wordCount(string in);
int sentCount(string in);
int CLindex(string in);

int main(void)
{
    string sentence = get_string("Text: ");
    int index = CLindex(sentence);
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
//count the number of words in a given text
int wordCount(string in)
{
    int count = 1;
    int length = strlen(in);
    for (int i = 0; i < length; i++)
    {
        if (in[i] == ' ')
        {
            count++;
        }
    }
    return count;
}
//count the number of letters in a given text
int letterCount(string in)
{
    int count = 0;
    int length = strlen(in);
    for (int i = 0; i < length; i++)
    {
        if (isalpha(in[i]))
        {
            count++;
        }
    }
    return count;
}
//count the number of sentences in a text
int sentCount(string in)
{
    int count = 0;
    int length = strlen(in);
    for (int i = 0; i < length; i++)
    {
        if (in[i] == '.' || in[i] == '!' || in[i] == '?')
        {
            count++;
        }
    }
    return count;
}

//calculate the coleman-liau index
int CLindex(string in)
{
    int index;
    //average letters per word
    float L = ((float)letterCount(in) / (float)wordCount(in) * 100);
    //average sentences per 100 words
    float S = ((float)sentCount(in) / (float)wordCount(in) * 100);
    //actual calculation
    index = round(0.0588 * L  - 0.296 * S - 15.8);
    return index;
}
