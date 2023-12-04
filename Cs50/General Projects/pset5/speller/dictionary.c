// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
//word counter
int count = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //hash the word to get the index
    int i = hash(word);
    //create a pointer aimed at that index
    node *cursor = table[i];
    //traverse the linked list
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }
    //read in the strings
    char buffy[LENGTH];
    char *buffer = &buffy[0];
    //adds in the nodes
    while (fscanf(dict, "%s", buffy) != EOF)
    {
        node *NewNode = malloc(sizeof(node));
        strcpy(NewNode->word, buffer);
        int index = hash(buffer);
        NewNode->next = table[index];
        table[index] = NewNode;
        count++;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //go through every index
    for (int i = 0; i < N; i++)
    {
        //set cursor and tmp as the first element of the list
        node *cursor = table[i];
        node *tmp = cursor;
        //go through every element
        while (cursor != NULL)
        {
            //move cursor to the next
            cursor = cursor->next;
            //free current
            free(tmp);
            //move temp to next
            tmp = cursor;
        }
    }
    return true;
}
