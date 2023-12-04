import csv
import sys


def main():

    # TODO: Check for command-line usage
    if (len(sys.argv) != 3):
        print(len(sys.argv))
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    namesDict = {}
    with open(sys.argv[1], "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:

            # A list of all strs shown in database
            keys = getKeys(row)

            # A list of all str quantities attached to a name
            values = getValues(row)

            namesDict[tuple(values)] = row.get('name')

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as infile:
        DNAreader = csv.reader(infile)
        for row in DNAreader:
            DNAseq = str(row)

    # TODO: Find longest match of each STR in DNA sequence
    STRlist = []
    for STR in keys:
        value = str(longest_match(DNAseq, STR))

        STRlist.append(value)

    # TODO: Check database for matching profiles
    STRlist = tuple(STRlist)
    if (STRlist in namesDict.keys()):
        out = namesDict.get(STRlist)
    else:
        out = "No match"

    print(out)
    return


# A function which gets all values in a dict as list, and pops element 0
def getValues(inRow):
    values = list(inRow.values())
    values.pop(0)
    return values


def getKeys(inRow):
    keys = list(inRow.keys())
    keys.pop(0)
    return keys


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
