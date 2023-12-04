# RROTUNDU 2023

# Main function
def main():
    sentence = input("Text: ")
    index = CLindex(sentence)
    if (index > 16):
        print("Grade 16+\n")
    elif (index < 1):
        print("Before Grade 1\n")
    else:
        print("Grade " + str(index) + "\n")

# wordCount(String in) function


def wordCount(inString):
    count = 1
    length = len(inString)
    for i in range(length):
        if (inString[i] == ' '):
            count += 1
    return count

# letterCount(String in) function


def letterCount(inString):
    count = 0
    length = len(inString)
    for i in range(length):
        if (inString[i].isalpha()):
            count += 1
    return count

# sentenceCount(String in) function


def sentenceCount(inString):
    count = 0
    length = len(inString)
    for i in range(length):
        if (inString[i] == '.' or inString[i] == '!' or inString[i] == '?'):
            count += 1
    return count

# CLindex(String in) function


def CLindex(inString):
    L = (float(letterCount(inString)) / float(wordCount(inString)) * 100)
    S = (float(sentenceCount(inString)) / float(wordCount(inString)) * 100)
    index = round(0.0588 * L - 0.296 * S - 15.8)
    return index


# main call
main()