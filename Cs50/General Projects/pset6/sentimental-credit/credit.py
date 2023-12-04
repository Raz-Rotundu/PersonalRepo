# RROTUNDU 2023

import sys


# Main function
def main():
    # Get user input as string for determining length
    numberString = input("Number: ")

    # Variable will hold the card type
    CardType = ""

    # Verify the card type
    if(isAmex(numberString)):
        CardType = "AMEX"

        if(not checkSum(numberString)):
            CardType = "INVALID"

    elif(isMaster(numberString)):
        CardType = "MASTERCARD"

        if(not checkSum(numberString)):
            CardType = "INVALID"

    elif(isVisa(numberString)):
        CardType = "VISA"

        if(not checkSum(numberString)):
            CardType = "INVALID"
    else:
        CardType = "INVALID"

    print("Number: " + numberString + "\n" + CardType)







# Boolean is it AMEX
def isAmex(numstr):
    # The length of the given string
    length = len(numstr)
    # That string converted to a number(should be all numbers anyways)
    number = int(numstr)

    if(length == 15):
        # Pow10 variables
        powTen = pow(10, length)
        divisor = pow(10, (length - 2))

        # Modulo of the last 2 digits
        lastTwo  = (number % powTen) / divisor

        if(lastTwo == 34 or lastTwo == 37):
            return True
        else:
            return False
    else:
        return False






# Boolean is it Mastercard
def isMaster(numstr):
    # The length of the given string
    length = len(numstr)
    # That string converted to a number(should be all numbers anyways)
    number = int(numstr)

    # Check length first
    if(length == 16):
         # Pow10 variables
        powTen = pow(10, length)
        divisor = pow(10, (length - 2))

        # Modulo of the last 2 digits
        lastTwo  = (number % powTen) / divisor
        #if (LastTwo == 51 || LastTwo == 52 || LastTwo == 53 || LastTwo == 54 || LastTwo == 55)
        if(lastTwo == 51 or lastTwo == 52 or lastTwo == 53 or lastTwo == 54):
            return True
        else:
            return False
    else:
        return False





# Boolean is it VISA
def isVisa(numstr):
    # The length of the given string
    length = len(numstr)
    # That string converted to a number(should be all numbers anyways)
    number = int(numstr)

    if(length == 13 or length == 16):
     # Pow10 variables
        powTen = pow(10, length)
        divisor = pow(10, (length - 1))

        lastOne = ((number % powTen) / divisor)

        if(lastOne == 4):
            return True
        else:
            return False
    else:
        return False







# Boolean is the checksum correct
def checkSum(numstr):
    length = len(numstr)
    longNum = int(numstr)
    total = otherSum(longNum, length) + lastSum(longNum, length)
    if (total % 10 == 0):
        return true
    else:
        return false



# Int does the other sum
def otherSum(inNum, length):
    x = 2
    sum = 0
    for i in len(length):
        pwr = pow(10, x)
        div = pow(10, x - 1)
        current = ((inNum % pwr) / div)
        #digit is multiplied by two
        current = current * 2
        #the result is then broken into individual digits, and added together

        z = 1
        while (z < 3):
            subpwr = pow(10, z)
            subdiv = pow(10, z - 1)
            subcurrent = ((current % subpwr) / subdiv)
            sum = sum + subcurrent
            z = z + 1
        x = x + 2
    return sum;

# Int does the final sum
def lastSum(inNum, length):
    x = 1
    sum = 0

    for i in length:
        pwr = pow(10, x)
        div = pow(10, x - 1)
        current = ((inNum % pwr) / div)
        #result is summed together
        sum = sum + current
        # printf("CURRENT: %li\n", current);
        #printf("SUM: %i\n", sum);
        x = x + 2
    return sum

main()