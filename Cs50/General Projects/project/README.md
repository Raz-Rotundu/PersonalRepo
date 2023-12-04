# AI Name Generator Website
#### Video Demo:  https://youtu.be/-tmWg-hB4Uo
#### Description:
### Program Overview:
The goal of the program is to implement a simple Markov chain on letter, letter pairs, and letter triples to generate some names, and then serve up these names to the user through a website. It is divided into two phases: the training phase, using a csv file to train the model, and a generation phase, which uses to model to come up with new names, and displays them to a website
#### Phase 1: Model training (markovNames)
IMPORTANT: THIS PART SHOULD BE EXECUTED FIRST BY RUNNING TRAINER.PY FROM THE COMMAND LINE
This phase uses a csv files provided by the US government displaying the most popular names of babies born in a given year, their sex, and the how many were born. This model has been adapted specifically to this csv format, but could easily be adapted to other csv files or even text files
##### fileReader.py
This file contains the functions which will convert the csv file into a workable text list of names.
OUTPUT: a txt file containing one name on each row
###### fileReader(filename, readmode, cutoff)
This function takes the name of a csv file, and 2 filters: readmode and cutoff
readmode is the sex filter. 'm' will use only male names, 'f' will use only female names
cutoff is the quantity filter. Any names under the given amount will be disregarded. Useful for only sampling the popular names
##### trainers.py
Three functions which generate the probabilities necessary for the mMarkov chains. One each for letter, pairs and triples.
OUTPUT: One txt file containing the probability that the name will start with the given unit, one txt file containing a dict of the following style:
{key = all possible combos, value={key = all possible combos, value= probability these combos will occur after the first key}}
NOTE: This is for each unit size(letter/pair/triple) for a total of 6 output files
###### letter(filename)
Reads through the text. For each letter in the alphabet, calculate the odds of each other letter occuring in the text.Convert this dict to a string and write it to a txt file of the form: (M/F)(letter/pair/triple).txt
###### pairs(filename)
Generate a set of all possible 2 letter combinations. For each pair in this set, calculate the odds of each other pair in the set occuring in the given text.Convert this dict to a string and write it to a txt file of the form: (M/F)(letter/pair/triple).txt. Trailing empty spaces are filled with newline chars.
###### triples()
Generate a set of all possible 3 letter combinations. For each triple in this set, calculate the odds of each other triple in the set occuring in the given text. Convert this dict to a string and write it to a txt file of the form: (M/F)(letter/pair/triple).txt. Trailing empty spaces are filled with newline chars.
###### getTotal(dict)
For a given dict of {key = unit, value = number of occurances}, calculate the total number of ocurrances across all keys
RETURN: integer Total
###### getAverages(dict, total)
Function takes a dict of frequencies, a total amount
RETURN: A dict of averages
###### createDoubles()
Function returns a list of all possible 2 letter combinations
###### createTriples()
Function returns a list of all possible 3 letter combinations
##### trainer.py
This pulls together the functions of fileReader.py and trainers.py to generate the requred txt files.
NOTE: this is what the user should interact with on the command line
###### main()
Generate the markov probabilities for all three resolution types. Will display the time it takes to generate each one
#### Phase 2: Model Output
This involves using the trained model to generate new names, and display them to the website
##### markovNames.nameWriter.py
This contains the functions required to convert the txt files back into dicts, generate a name, and then clean it up by removing the newlines
###### toDict(filename)
Takes the name of an existing file, returns is as a dict by using json.loads
###### makeName(mode)
The Phase one outputs txt files of the form: (M/F)(letter/pair/triple).txt. By passing the appropriate mode it will access the specified model file to use when generating the name.
###### hasNewline(string)
Checks if the string has a newline character. Returns T if yes, F if no
###### cleanUp(name)
removes all newline characters in given string
##### app.py, templates, requirements.txt, static
The components to a simple website. The user selects the gender of their child, and the website then produces 5 names. The user has the option of getting another five, or returnig home.

