import nltk
import sys

#test
nltk.download('punkt')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> Sent | Sent Conj Sent
Sent -> NP VP

PP -> P NP
AP -> Adj | Adj AP

AN -> AP N | N Ap | N

NP -> N
NP -> Det N | AN | N PP
NP -> Det AN | Det N PP | AN PP
NP -> Det AN PP

VP -> V | V NP | V PP
VP -> Adv VP | VP Adv
VP -> VP Conj VP


"""
# NP = noun phrase, a group of words (adjectives, ) connecting to a noun
# What to do with Adv, Conj, Det, P
# VP = verb phrase, a group of words () connecting to a verb
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize sentence based on words
    wordList = nltk.word_tokenize(sentence)

    # Output
    vals = []



    # Remove any words which do not have at least one alphabetical
    for word in wordList:
        alpha = 0
        for char in word:
            if char.isalpha():
                alpha += 1
        if alpha > 0:
            word = word.lower()
            vals.append(word)

    #Return cleaned list
    return vals




def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # The list with all of the noun phrase chunks
    list = []

    subtrees = tree.subtrees(filter = lambda t : t.label() == "NP")
    for st in subtrees:
        test = st.productions()
        # Proper chunk or no
        Extra_NP = False
        # If there's another NP somewhere beyond the first, it's not proper chunk
        for i in range(1, len(test)):
            c = str(test[i])
            if "NP" in c:
                Extra_NP = True
        if not Extra_NP:
            list.append(st)


    return list


if __name__ == "__main__":
    main()
