# rrotundu 2023
import sys

def main():
    #get the height
    height = int(input("Height? "))
    RowPrint(height)

def RevPrint(row, height):
    #TODO
    for i in (height - row):
        print(" ")
    ColPrint(row)

def RowPrint(x):
    #TODO
    for i in (x + 1):
        RevPrint(i, x)
        print("  ")
        ColPrint(i)
        print("/n")

def ColPrint(y):
    for q in y:
        print("#")



