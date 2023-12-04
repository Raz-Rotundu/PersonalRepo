#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    //iterate through all candidates
    for (int i = 0; i < candidate_count; i++)
    {
        //if the specified candidate exists, incement vote
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    //specified candidate does not exist
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int max = -1;
    //array to store potential winners
    string winner[candidate_count];
    //index to keep track of fillr
    int fill = 0;
    //first find the max
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > max)
        {
            max = candidates[i].votes;
            winner[0] = candidates[i].name;
        }
    }
    //go through the candidate list
    for (int i = 0; i < candidate_count; i++)
    {
        //go through the winner list
        for (int j = 0; j <= fill; j++)
        {
            //match ties, if the given candidate has same score as max, but different name
            if (candidates[i].votes == max && strcmp(candidates[i].name, winner[j]) != 0)
            {
                fill++;
                winner[fill] = candidates[i].name;
            }
        }
    }
    //print off all winners
    //If there is only one winner
    if (fill == 0)
    {
        printf("%s\n", winner[0]);
    }
    //if there are multiple
    else
    {
        for (int h = 0; h <= fill; h++)
        {
            printf("%s\n", winner[h]);
        }
    }
    return;
}
