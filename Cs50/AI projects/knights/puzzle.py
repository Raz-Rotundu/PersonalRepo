from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

gamerules = And(
    # A person is either a knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),

    # A person cannot be a knight and a Knave at the same time
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave))
)
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    gamerules,
    # If A is a knight, this is true
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a Knave, this is false
    Implication(AKnave, Not(And(AKnight,AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    gamerules,

    # A is a knight, this is true
    Implication(AKnight, And(AKnave, BKnave)),

    # If A is a knave, this is false
    Implication(AKnave, Not(And(AKnave, BKnave)))
    
    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    gamerules,

    # If A is a Knight, then AB are either both knights or knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave,BKnave))),

    # If A is a Knave, then they are different kinds
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave,BKnave)))),

    # If B is a knight, then they are different kinds
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave,BKnave)))),

    # If B is a knave, then they are the same
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave,BKnave)))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    gamerules,

    # Leave A for later
    # If A is a knight, then it is either a knight or knave?
    Implication(AKnight, Or(AKnight, AKnave)),
    #If A is a knave, then this isn't true
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    
    # Leave this B for later
    # If B is a knight, and A is a knight, then A is a knave
    Implication(And(AKnight,BKnight), AKnave),
    # If B is a knight, but A is not, then A has lied
    Implication(And(BKnight, AKnave), Not(AKnave)),
    # If B is a knave, but A is a knight then A did not say I am a knave
    Implication(And(BKnave, AKnight), Not(AKnave)),
    # If both are knaves...
    Implication(And(BKnave, AKnave), AKnight),

    # If B is a knight, c is a knave
    Implication(BKnight, CKnave),
    # If B is a knave, c is a knight
    Implication(BKnave, CKnight),

    # If C is a knight, A is one as well
    Implication(CKnight, AKnight),
    # If C is a knave, so is B
    Implication(CKnave, AKnight)
    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
