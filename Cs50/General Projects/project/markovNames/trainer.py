# Razvan Rotundu 2023

#This function takes a filename, processes it using fileReader, then outputs 4 .txt files:
#1. A processed names file 2. Markov odds for single letter, 3.Markov odds for double, 4.Markov odds for triples

#all the helper functions we'll need
from trainers import letter, pairs, triple
from fileReader import fileReader

#for checking command lines
import sys

# Test for timing
import time

def main():

    #chech the command line args
    if (len(sys.argv) != 4):
        print("USAGE: python filetrainer.py <textfile>.csv m/f, cutoff")
        return
    else:
        start = time.time()
        namesfile = (fileReader(sys.argv[1], sys.argv[2], sys.argv[3]))

        letterprobs = letter(namesfile)
        print("Letter probabilities calculated in {:.2f}s".format(time.time() - start))
        pairprobs = pairs(namesfile)
        print("Pair probabilities calculated in {:.2f}s".format(time.time() - start))
        tripleprobs = triple(namesfile)
        print("Triple probabilities calculated in {:.2f}s".format(time.time() - start))

main()
