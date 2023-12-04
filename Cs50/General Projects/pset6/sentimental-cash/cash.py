# rrotundu 2023
from math import floor


def main():
    change = -1
    while (change < 0):
        try:
            change = float(input("Change owed: "))
        except ValueError:
            change = float(input("Change owed: "))
    numcoins = getCoins(change)
    print(numcoins)


def getCoins(inFloat):
    curr = inFloat
    numquarters = floor(curr/0.25)
    curr = round((curr % 0.25), 2)
    print("Number of Quarters: " + str(numquarters) + "\nLeft over: " + str(curr) + "------------------\n")
    numdimes = floor(curr/0.1)
    curr = round((curr % 0.1), 2)
    print("Number of dimes: " + str(numdimes) + "\nLeft over: " + str(curr) + "------------------\n")
    numnickels = floor(curr/0.05)
    curr = round((curr % 0.05), 2)
    print("Number of Nickels: " + str(numnickels) + "\nLeft over: " + str(curr) + "------------------\n")
    numpennies = floor(curr/0.01)
    curr = round((curr % 0.01), 2)
    print("Number of pennies: " + str(numpennies) + "\nLeft over: " + str(curr) + "------------------\n")
    return (numquarters + numdimes + numnickels + numpennies)


main()