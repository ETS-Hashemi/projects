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
    if board[action[0]][action[1]] is not EMPTY:
        raise NotImplementedError

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    try:
        for i in range(3):
            for j in range(3):
                if board[i][0] == board[i][1] == board[i][2] == X:
                    return X
                elif board[i][0] == board[i][1] == board[i][2] == O:
                    return O
                elif board[j][j] == board[j+1][j+1] == board[j+2][j+2] == X:
                    return X
                elif board[j][j] == board[j+1][j+1] == board[j+2][j+2] == O:
                    return O
                elif board[0][0] == board[1][1] == board[2][2] == X:
                    return X
                elif board[0][0] == board[1][1] == board[2][2] == O:
                    return O
                elif board[0][2] == board[1][1] == board[2][0] == X:
                    return X
                elif board[0][2] == board[1][1] == board[2][0] == O:
                    return O
        return None
    except:
        raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    try:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
        if winner(board) is not None:
            return True
    except:
        raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    try:
        if terminal(board):
            if winner(board) == X:
                return 1
            elif winner(board) == O:
                return -1
            else:
                return 0
    except:
        raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is over, return None (no moves left)
    if terminal(board):
        return None

    # Determine the current player (X or O)
    player_turn = player(board)
    optimal_action = None

    # If the current player is X (maximizing player)
    if player_turn == X:
        v = -math.inf  # Initialize the value to negative infinity
        # Iterate over all possible actions
        for action in actions(board):
            # Get the minimum value of the resulting board state
            min_val = min_val(result(board, action))
            # If the value is greater than the current value, update the value and optimal action
            if min_val > v:
                v = min_val
                optimal_action = action

    # If the current player is O (minimizing player)
    else:
        v = math.inf  # Initialize the value to positive infinity
        # Iterate over all possible actions
        for action in actions(board):
            # Get the maximum value of the resulting board state
            max_val = max_val(result(board, action))
            # If the value is less than the current value, update the value and optimal action
            if max_val < v:
                v = max_val
                optimal_action = action

    # Return the optimal action for the current player
    return optimal_action
