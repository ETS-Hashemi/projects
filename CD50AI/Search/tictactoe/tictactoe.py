"""
Tic Tac Toe Player
"""

import math

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
    try:
        if board == initial_state():
            return X
        else:
            count_X = 0
            count_O = 0
            for row in board:
                for cell in row:
                    if cell == X:
                        count_X += 1
                    elif cell == O:
                        count_O += 1
            if count_X < count_O:
                return X
            else:
                return O
    except:
        raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    try:
        set = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    set.append((i, j))
        return set
    except:
        raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
 X   """
    raise NotImplementedError
