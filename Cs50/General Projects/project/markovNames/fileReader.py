#Razvan Rotundu 2023

#This program takes a name csv file, and writes out a list of all the names only to a txt file, tool used to pull names by gender from csv file
#NOTE: This function assumes the given file actually exists

import sys
import csv
from pathlib import Path

#name, sort by male or female, cutoff for qty.
def fileReader(filename, readmode, cutoff):
    # Check for right amount of args
    # check proper arguments
    if (not filename):
        print("USAGE: python fileReader.py textfile.txt, readmode, cutoff")
        return
    if (not readmode):
        print("USAGE: python fileReader.py textfile.txt, readmode, cutoff")
    else:
        #store the mode as a variable
        mode = readmode.upper()

        #first we open the file, saving all of the names as dicts {Name: Sex: Qty: }
        with open(filename, "r") as file:

            #The reader object
            reader = csv.DictReader(file)

            #the list which will then be written to file
            nameslist = []


            for row in reader:
                nameslist.append(row)

            #close the file
            file.close()

        #Then we create the output file
        outname = mode + "Names.txt"

        with open(outname, "w") as file:

            if not cutoff:
                #do all entries if no input given
                for i in nameslist:
                    if (i['Sex'] == mode):
                        file.write(i['Name'] + "\n")


            #entries if input given
            else:
                for i in nameslist:
                    if (i['Sex'] == mode) and (int(i['Qty']) > int(cutoff)):
                        file.write(i['Name'] + "\n")

            file.close()

            # A name passed to the markov maker functions
            return outname