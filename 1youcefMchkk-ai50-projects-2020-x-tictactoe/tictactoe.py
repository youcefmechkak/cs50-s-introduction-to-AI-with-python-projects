"""
Tic Tac Toe Player
"""

import math
from tkinter.tix import MAX

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
    x_num = 0
    o_num = 0

    for row in board :
        for element in row :
            if element == X :
                x_num = x_num + 1
            elif element == O :
                o_num = o_num + 1


    if x_num == o_num :
        return X
    
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    action_set = list ()

    
    for i in [0, 1 ,2] :
        for j in [0, 1 ,2] :
            if board[i][j] == EMPTY :
                tmp_cell = (i , j)
                action_set.append (tmp_cell)

    return action_set

    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # create a new board
    new_board = list()
    # copy the board to the new board
    for row in board :
        new_row = list ()

        for cell in row :
            new_row.append (cell)
        
        new_board.append(new_row)



    # add the action
    if new_board [action[0]][action[1]] == EMPTY :
        new_board [action[0]][action[1]] = player(board)
        return new_board


    #if you can't add the action raise an exception

    raise NameError("action can't be taken") 


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # the diagonal case
    if board[0][0] == board [1][1] and board [0][0] == board [2][2] :
        if board [0][0] == X :
            return X
        elif board [0][0] == O :
            return O

    if board[0][2] == board [1][1] and board [0][2] == board [2][0] :
        if board [0][2] == X :
            return X
        elif board [0][2] == O :
            return O

    
    # the other cases

    for num in [0 , 1 , 2] :
        
        # checking the row
        if board[num][0] == board[num][1] and board[num][0] == board[num][2] :
            if board [num][0] == X :
                return X
            elif board [num][0] == O :
                return O

        # checking the column
        if board[0][num] == board[1][num] and board[0][num] == board[2][num] :
            if board [0][num] == X :
                return X
            elif board [0][num] == O :
                return O


    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    # if there is a winner
    if winner (board) == X or winner (board) == O :
        return True

    # if the board is filled
    for row in board :
        for cell in row : 
            if cell == EMPTY :
                return False
    
    return True
    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)

    if result == X :
        return 1
    elif result == O :
        return -1
    else :
        return 0





def min_value (board) :
    if terminal(board) :
        return utility (board)


    v = math.inf

    for action in actions(board) :
        v = min (v, max_value(result(board, action)))

    return v


def max_value (board) :
    if terminal(board) :
        return utility (board)


    v = -math.inf

    for action in actions(board) :
        v = max (v, min_value(result(board, action)))

    return v




# pick an action from actions(state) that produce the highest utility
def maximum (board) :

    v = -math.inf

    for action in actions(board) :
        if v < min_value (result(board, action)) :
            v = min_value (result(board, action))
            optimal_action = action

    return optimal_action


def minimum (board) :
    v = math.inf

    for action in actions(board) :
        if v > max_value (result(board, action)) :
            v = max_value (result(board, action))
            optimal_action = action

    return optimal_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
     
    if player (board) == X :
        return maximum (board)
    else :
        return minimum (board)
