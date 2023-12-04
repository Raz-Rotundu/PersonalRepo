# rrotundu 2023
import sys


def main():
    # get the height
    height = input("Height? ")

    # if not numeric, keep asking
    while (not height.isnumeric()):
        height = input("Height? ")

    # if not in range keep asking
    while (int(height) < 1 or int(height) > 8):
        height = input("Height? ")
        # if they give a non numeric, ask again
        while (not height.isnumeric()):
            height = input("Height? ")

    # do the program
    RowPrint(int(height))


def RevPrint(row, height):
    for i in range(height - row):
        print(" ", end="")
        i += 1
    ColPrint(row)


def RowPrint(x):
    i = 1
    while (i < (x + 1)):
        RevPrint(i, x)
        print("  ", end="")
        ColPrint(i)
        print("")
        i += 1


def ColPrint(y):
    for q in range(y):
        print("#", end="")
        q += 1

# A function to check if the string is alphabetical(bad)


main()

