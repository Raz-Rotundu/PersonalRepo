# Razvan Rotundu 2023
# This file contains the list of all the trainer functions(single, double, triple)
#NOTE: These functions all assume the file  actually exists



# The function for single letter markov chains
def letter(filename):
    # check proper arguments
    if (not filename):
        print("USAGE: letter.py(<textfile>.txt)")
        return

    else:
        # the alphabet used to iterate for every letter
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        # this dict will have the probability of each letter occuring {key = letter, Value = dict of probabilities}, INCLUDES "/n"
        probabilities = {}

        #This dict will have the frequency of each letter occuring in the text
        freq = {}
        prob = {}

        # for each letter
        for char in alphabet:

            # set up a dict measuring the  number occurance of each subsequent letter { a: #, b: # .....}
            frequency = {}

            with open(filename, "r") as file:

                names = file.readlines()

                #go through name by name
                for name in names:

                    #go through letter by letter
                        for i in range(len(name)):

                            #if the next value does not exist, we are at the last letter
                            if (i + 1) not in range(len(name)):
                                 break
                            curr = name[i].lower()
                            next = name[i + 1].lower()

                            if curr == char:
                                 #This part is used to compute frequency of letters at the start of names
                                 if i == 0:
                                    if curr not in freq:
                                        freq[curr] = 1
                                    else:
                                        freq[curr] += 1

                                 if next not in frequency:
                                      frequency[next] = 1
                                 else:
                                      frequency[next] += 1
                # now we have a dict of frequencies for each individual letter

                total = getTotal(frequency)

                probabilities[char] = getAverages(frequency, total)



        #compute the average occurance of each unit
        utotal = getTotal(freq)
        for key in freq:
            prob[key] = float(freq[key]/utotal)
        oname = filename[0] + filename[1] + "letterFreq.txt"
        with open(oname, "wt") as file:
            file.write(str(prob))
        file.close()

        #write out the data we just compiled to a file
        outname = filename[0] + filename[1] + "letters.txt"
        with open(outname, "wt") as file:
             file.write(str(probabilities))
        file.close()
        # Name of the file written out to
        return outname

# The function for double letter chains
def pairs(filename):

    # check proper arguments
    if (not filename):
        print("USAGE: pairs.py(<textfile>.txt)")
        return

    else:
        #compute every possible letter pair
        pairs  = createDoubles()

        # this dict will have the probability of each double occuring {key = double, Value = dict of probabilities}, INCLUDES "/n"
        probabilities = {}

        #This dict will have the frequency of each letter occuring in the text
        freq = {}
        prob = {}

        # for each letter
        for double in pairs:

            # set up a dict measuring the  number occurance of each pair { a: #, b: # .....}
            frequency = {}

            with open(filename, "r") as file:

                names = file.readlines()

                 # go through name by name
                for name in names:

                    # Go through pair by pair
                    for i in range(0,len(name), 2):

                        # Put together the first double,
                        if (i + 1) not in range(len(name)):
                            #no double exists to compare
                            break
                        if (i + 2) not in range(len(name)):

                            #no subsequent double exists
                            break
                        if (i + 3) not in range(len(name)):

                            #fill with terminator \n
                            fourth = "\n"
                        else:
                            fourth = name[i + 3]

                        # Now we have the current pair, and the following
                        curr = (name[i]+name[i + 1]).lower()
                        next = (name[i + 2] + fourth).lower()

                        #check if we have an instance of current double
                        if curr == double:
                            #This part is used to compute frequency of letters at the start of names
                            if i == 0:
                                if curr not in freq:
                                    freq[curr] = 1
                                else:
                                    freq[curr] += 1

                            if next not in frequency:
                                frequency[next] = 1
                            else:
                                frequency[next] += 1


                # now we have a dict of frequencies for each individual pair
                total = getTotal(frequency)

                probabilities[double] = getAverages(frequency, total)

        #compute the average occurance of each unit
        utotal = getTotal(freq)
        for key in freq:
            prob[key] = float(freq[key]/utotal)
        oname = filename[0] + filename[1] + "pairFreq.txt"
        with open(oname, "wt") as file:
            file.write(str(prob))
        file.close()

        #write out the data we just compiled to a file
        outname = filename[0] + filename[1] + "pairs.txt"
        with open(outname, "wt") as file:
             file.write(str(probabilities))
        file.close()
        # Name of the file written out to
        return outname

# The function for triple letter chains
def triple(filename):

     # check proper arguments
    if (not filename):
        print("USAGE: triple.py(<textfile>.txt)")
        return

    else:
        #compute every possible letter pair
        triples  = createTriples()

        # this dict will have the probability of each double occuring {key = double, Value = dict of probabilities}, INCLUDES "/n"
        probabilities = {}

        #This dict will have the frequency of each letter occuring in the text
        freq = {}
        prob = {}

        for triple in triples:

            # set up a dict measuring the  number occurance of each pair { a: #, b: # .....}
            frequency = {}

            with open(filename, "r") as file:

                names = file.readlines()

                 # go through name by name
                for name in names:

                    # Go through pair by pair
                    for i in range(0,len(name), 3):

                        # Put together the first triple
                        if (i + 1) not in range(len(name)):
                            #no triple exists to compare
                            break
                        if (i + 2) not in range(len(name)):
                            #no triple exists to compare
                            break

                        # Put together the second triple
                        if (i + 3) not in range(len(name)):
                            #no subsequent triple exists
                            break
                        if (i + 4) not in range(len(name)):
                            #fill gap with newline
                            fifth = "\n"
                        else:
                            fifth = name[i+4]
                        if (i + 5) not in range(len(name)):
                            #fill gap with newline
                            sixth = "\n"
                        else:
                            sixth = name[i+5]


                        # Now we have the current triple, and the following one
                        curr = (name[i] + name[i + 1] + name[i + 2]).lower()
                        next = (name[i + 3] + fifth + sixth).lower()

                        #HMMMMM Maybe 4 letter mix will work better
                        #next = (name[i + 2] + name[i + 3] + fifth + sixth).lower()

                        #check if we have an instance of current double
                        if curr == triple:
                            #This part is used to compute frequency of letters at the start of names
                            if i == 0:
                                if curr not in freq:
                                    freq[curr] = 1
                                else:
                                    freq[curr] += 1

                            if next not in frequency:
                                frequency[next] = 1
                            else:
                                frequency[next] += 1


                # now we have a dict of frequencies for each individual triple
                total = getTotal(frequency)

                probabilities[triple] = getAverages(frequency, total)

        #compute the average occurance of each unit
        utotal = getTotal(freq)
        for key in freq:
            prob[key] = float(freq[key]/utotal)
        oname = filename[0] + filename[1] + "tripleFreq.txt"
        with open(oname, "wt") as file:
            file.write(str(prob))
        file.close()

        #write out the data we just compiled to a file
        outname = filename[0] + filename[1] + "triples.txt"
        with open(outname, "wt") as file:
             file.write(str(probabilities))
        file.close()
        # Name of the file written out to
        return outname



# helper functions used in the various resolution methods

# Function takes a dict, returns total amount of all values(assumes int)
def getTotal(dict):
    total = 0
    for key in dict:
        # Get the number
        num = dict[key]

        #check if it is an integer
        if isinstance(num, int):
            total += num

        #if not, return nothing
        else:
            return

    return total

# Function takes a dict of frequencies, a total amount, returns a dict of averages
def getAverages(dict, total):
    avg = dict

    for key in dict:
        # Set the key to be its current value divided by the toal, limited to 3 decimal places
        # Try non-formatted
        #dict[key] = "{:.4f}".format(float(dict[key]) / float(total))
        dict[key] = float(dict[key]) / float(total)

    return avg

# Funtion which computes every possible combination of 2 letters, returns a list of them in lowercase
def createDoubles():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    doubles = []
    for letter1 in alphabet:
        for letter2 in alphabet:
            doubles.append(letter1 + letter2)
    return doubles

# Function which computes every possible combination of 3 letters, returns a list of them in lowercase
def createTriples():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    triples = []
    for letter1 in alphabet:
        for letter2 in alphabet:
            for letter3 in alphabet:
                triples.append(letter1+letter2+letter3)
    return triples

