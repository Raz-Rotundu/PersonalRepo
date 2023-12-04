"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X has the first move
    if board == initial_state():
        return X
    # Check if there are more xs or os
    else:
        numx = 0
        numo = 0
        for row in board:
            for element in row:
                if element == X:
                    numx += 1
                elif element == O:
                    numo += 1
        if numx > numo:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # The set of all possible action on given board
    actionSet = set()

    #go through each square in the 3x3 grid
    for i in range(3):
        for j in range(3):
            # If not occupied by x and not occupied O, it is free
            if not ((board[i][j] == X) or (board[i][j] == O)):
                tuple = (i,j)
                actionSet.add(tuple)
    return actionSet


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Make a deep copy of the board
    cboard = copy.deepcopy(board)
    # Get the player who's turn it is
    thisplayer = player(board)
    # Check if move is valid( square is empty)
    if cboard[action[0]][action[1]] == EMPTY:

        # Do the move
        cboard[action[0]][action[1]] = thisplayer
    else:
        raise ValueError
    
    # Return the board
    return cboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # The scores array we're checking with [row1, row2, row3, col1, col2, col3, diag1, diag2]
    scores = [0,0,0,0,0,0,0,0,]

    # The coordinates of the forwards and backwards diagonal
    diag1 = {(0,0), (1,1), (2,2)}
    diag2 = {(0,2), (1,1), (2,0)}
    # Check for x win
    # Win condition for x: any value in scores is 3

    # For each element on the board
    for row in range(3):
        for column in range(3):
            element = board[row][column]
            # Check if x, o, or none
            if element == X:
                value = 1
            elif element == O:
                value = -1
            else:
                value = 0
            # Add value to relevant row and column
            scores[row] += value
            #correct for the rows
            scores[column + 3] += value
            
            # compute coord
            coord = (row, column)
            # Check if in diagonal
            if coord in diag1:
                scores[6] += value
            if coord in diag2:
                scores[7] += value
    # Now verify the scores values, if there is a +3, x has won, -3 o has won
    for i in range(len(scores)):
        if scores[i] == 3:
            return X
        if scores[i] == -3:
            return O
    # Return None if neither has won
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if someone has won
    #winner = winner(board)

    # If no winner
    if not winner(board):
        # Check if there is any more available spots
        for i in range(3):
            for j in range(3):
                # If there is an available spot, game is not over
                if board[i][j] == None:
                    return False
        return True
    # Else there either is a winner, or there are no available spots left, so game over
    else:
        return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Get the winner
    thiswinner = winner(board)

    # Check the value and return the proper one
    if thiswinner == X:
        return 1
    elif thiswinner == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Base case
    if terminal(board):
        return None
    
    # The set of all possible actions at this state. Which is best?
    moves = actions(board)

    # Who is the computer playing as?
    playa  = player(board)

    # Value to be returned
    act = None

    # o player is minimizing,  x player is maximizing
    if playa == X:
        # The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a))
        # Init maxval to large negative
        maxval = -99999999

        # For each move
        for move in moves:
         
         # Evaluate its utility
         value = Minvalue(result(board, move))

         # If the utiliy is greater than current candidate, set it as top move, update maxval
         if value > maxval:
             maxval = value
             act = move
    else:
        # The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).
        minval = 100000

        for move in moves:
            value = Maxvalue(result(board, move))
            if value < minval:
                minval = value
                act = move
    
    return act


# Max value function is helper for minimax
def Maxvalue(board):
    v = -99999999999

    #problem 
    if terminal(board):
        return utility(board)
    
    # For each tuple in the set
    for action in actions(board):
        v = max(v,Minvalue(result(board, action)))
    return v

# Min vlaue function is helper for minimax
def Minvalue(board):
    v = 9999999999
    
    #problem here
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v,Maxvalue(result(board, action)))
    return v


