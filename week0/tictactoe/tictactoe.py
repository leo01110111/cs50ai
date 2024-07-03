"""
Tic Tac Toe Player
"""

import math, copy

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

def read(board):
    """
    Returns the coordinates of all the X'S, O'S and EMPTY's on the board as tuples of lists of tuples. This is used by most of the functions below. 
    """
    xcoords = []
    ocoords = []
    ecoords = []
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == X:
                xcoords.append((i,j))
            elif board[i][j] == O:
                ocoords.append((i,j))
            elif board[i][j] == EMPTY:
                ecoords.append((i,j))
    return (xcoords, ocoords, ecoords)

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    coords = read(board)
    xcount = len(coords[0])
    ocount = len(coords[1])

    if xcount == 0 and ocount == 0:
        return X
    elif xcount > ocount:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    coords = read(board)
    return coords[2]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        print(action, "out of", actions(board))
        raise LookupError
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Checks for straight lines
    for i in range(0,3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    
    #Checks for diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #If one side wins
    if winner(board) is not None:
        return True
    
    #Filled board with no winners
    coords = read(board)
    if len(coords[0]) == 5:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    victor = winner(board)
    if victor is X:
        return 1
    elif victor is O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) is True:
        return None
    
    if player(board) == X:
        v = -2
        best_action = None
        for action in actions(board):
            if min_value(result(board, action)) > v:
                best_action = action
                v = min_value(result(board, action))
        print(best_action)
        return best_action

    elif player(board) == O:
        v = 2
        best_action = None
        for action in actions(board):
            if max_value(result(board, action)) < v:
                best_action = action
                v = max_value(result(board, action))
        print(best_action)
        return best_action
    

def max_value(board):
    v = -2
    if terminal(board) == True:
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
    

def min_value(board):
    v = 2
    if terminal(board) == True:
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v