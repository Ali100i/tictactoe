"""
Tic Tac Toe Player
"""

from logging import exception
import math
from copy import deepcopy
from multiprocessing.sharedctypes import Value
from pickle import FALSE, TRUE
import math
from queue import Empty

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
    countX = 0
    countO = 0

    for i in board:
        for j in i:
            if (j==X):
                countX +=1
            elif (j == O):
                countO += 1
    if(countX > countO):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionSet = set()

    for i in range(len(board)):
        for j in range(len(board)):
            if (board[i][j] == EMPTY):
                actionSet.add((i,j))

    return actionSet

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    w = action[0]
    z = action[1]

    # checking if the numbers are within the dimensions of the game
    if ((w==0 or w==1 or w==2) and (z==0 or z==1 or z==2)):
        # checking if the selected cell is empty.
        if(board[w][z] == EMPTY):
            board_copy = deepcopy(board)
            board_copy[w][z] = player(board)
            return board_copy
        else:
            raise Exception("The cell you are trying to access is occupied.")
    else:
        raise Exception("This is not a valid action.")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # checking if X or O won horizontally  
    for i in range(3):
        countX = 0
        countO = 0
        for j in range(3):
            if(board[i][j] == X):
                countX += 1
            elif(board[i][j] == O):
                countO += 1
        if(countX == 3):
            return X
        elif(countO == 3):
            return O
        

    # checking if X or O won vertically
    for j in range(3):
        col = ''
        for i in range(3):
            if(board[i][j] == X):
                col += 'X'
            elif(board[i][j] == O):
                col += 'O'
        if(col == 'XXX'):
            return X
        elif(col == 'OOO'):
            return O
    
    # checking if X or O won diagonally
    diagonalLine1 = ''
    diagonalLine2 = ''
    j = 2
    # from top left to bottom right cell
    for i in range(3):
        if(board[i][i] == X):
            diagonalLine1 += 'X'
        elif(board[i][i] == O):
            diagonalLine1 += 'O'
    # from top right to bottom left cell 
    for i in range(3):
        if(board[i][j] == X):
            diagonalLine2 += 'X'
        elif(board[i][j] == O):
            diagonalLine2 += 'O'
        j -= 1

    if(diagonalLine1 == 'XXX' or diagonalLine2 == 'XXX'):
        return X
    elif(diagonalLine1 == 'OOO' or diagonalLine2 == 'OOO'):
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board)):
        return True

    # In the case of a tie or unfinished game :-
    else:
        countFilledCells = 0
        for i in range (3):
            for j in range(3):
                if (board[i][j] != EMPTY):
                    countFilledCells += 1
        if(countFilledCells == 9):
            return TRUE
        else:
            return False

    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) == 'X'):
        return 1

    elif (winner(board) == 'O'):
        return -1

    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # This function is gonna return the best move after getting the best score for the AI from minimax_helper function.
    def OptimalMove(maxPlayer):
        if(maxPlayer): # If the AI is the maximizing player
            bestScore = -math.inf
            bestMove = None
            for i in range(3):
                for j in range(3):
                    if(board[i][j] == EMPTY):
                        board[i][j] = player(board)
                        score = minimax_helper(board,3,False)
                        board[i][j] = EMPTY
                        if(score > bestScore):
                            bestScore = score
                            bestMove = (i,j)
            return bestMove
        else: # If the AI is the minimizing player
            bestScore = math.inf
            bestMove = None
            for i in range(3):
                for j in range(3):
                    if(board[i][j] == EMPTY):
                        board[i][j] = player(board)
                        score = minimax_helper(board,3,True)
                        board[i][j] = EMPTY
                        if(score < bestScore):
                            bestScore = score
                            bestMove = (i,j)
            return bestMove

    # this is gonna return the best score to the AI with respect to it being either the maximizing or the minimizing player. 
    def minimax_helper(board,max_depth,maximizingPlayer):
        # helper function for minimax
        if(terminal(board)):
            return utility(board)
        
        if(maximizingPlayer):
            value = -math.inf
            for i in range(3):
                for j in range(3):
                    if(board[i][j] == EMPTY):
                        board[i][j] = player(board)
                        eval = minimax_helper(board,max_depth+1,False)
                        board[i][j] = EMPTY
                        value = max(value,eval)
            return value
                        
        else:
            value = math.inf
            for i in range(3):
                for j in range(3):
                    if(board[i][j] == EMPTY):
                        board[i][j] = player(board)
                        eval = minimax_helper(board,max_depth+1,True)
                        board[i][j] = EMPTY
                        value = min(value,eval)
            return value

    # If the game finished None will be returned
    if(terminal(board)):
        return None
    
    # Otherwise The AI will get the best move.
    if(player(board) == 'X'):
        bestMove = OptimalMove(True)
        return bestMove
    else:
        bestMove = OptimalMove(False)
        return bestMove
        