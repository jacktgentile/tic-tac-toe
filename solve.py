# -*- coding: utf-8 -*-

"""
This is the function you will implement. It will take in a numpy array of the board
as well as a list of n tiles in the form of numpy arrays. The solution returned
is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
where pi is a tile (may be rotated or flipped), and (rowi, coli) is
the coordinate of the upper left corner of pi in the board (lowest row and column index
that the tile covers).

-Use np.flip and np.rot90 to manipulate pentominos.

-You can assume there will always be a solution.
"""
import numpy as np
translation_list = []

# test if a board is complete i.e. all elements are non-zero
def goal_test(board):
    for row in board:
        for i in row:
            if i == 0:
                return False
    return True

# returns true if you can place tile at location given the state of the board
def can_place_tile(board, tile, location):
    r = location[0]
    c = location[1]
    h = tile.shape[0]
    w = tile.shape[1]
    for i in range(0,h):
        for j in range(0,w):
            if tile[i][j] != 0 and board[r+i][c+j] != 0:
                return False
    return True

# modifies the board to include the tile. Assumes you can place tile there
def assign_tile(board, tile, location):
    r = location[0]
    c = location[1]
    h = tile.shape[0]
    w = tile.shape[1]
    board[r : r+h, c : c+w] += tile

def list_contains(mylist, item):
    for curitem in mylist:
        flag = False
        if curitem.shape == item.shape:
            for i in range(0,item.shape[0]):
                for j in range(0,item.shape[1]):
                    if item[i][j] != curitem[i][j]:
                        flag = True
                        break
                if flag:
                    break
            if not flag:
                return True
    return False

def unassign_tile(board, tile, location):
    r = location[0]
    c = location[1]
    h = tile.shape[0]
    w = tile.shape[1]
    board[r : r+h, c : c+w] -= tile

# recursive helper function for solve
def solve_r(board, pents, sol):
    if len(pents) == 0 or goal_test(board):
        return True
    current_pent = pents.pop()
    for i in range(0,board.shape[0] - current_pent.shape[0]):
        for j in range(0,board.shape[1] - current_pent.shape[1]):
            if can_place_tile(board, current_pent, (i,j)):
                assign_tile(board, current_pent, (i,j))
                if board[i][j] != 0 and solve_r(board, pents, sol):
                    return True
    return False


def solve(board, pents, app=None):
    # our_board[i][j] is value in domino at that spot, 0 if unassigned
    our_board = np.zeros_like(board)
    my_sol = []

    for pent in pents:
        pentcpy = pent.copy()
        trans_pent = []
        for i in range(0,4):
            if not list_contains(trans_pent, pentcpy):
                trans_pent.append(pentcpy)
            pentcpy = np.rot90(pentcpy)
        pentcpy = np.flip(pentcpy, 0)
        for i in range(0,4):
            if not list_contains(trans_pent, pentcpy):
                trans_pent.append(pentcpy)
            pentcpy = np.rot90(pentcpy)
        print(trans_pent)
        translation_list.append(trans_pent)

    our_pents = pents.copy()
    solve_r(our_board, our_pents, my_sol)
    if app is not None:
        app.draw_solution_and_sleep(my_sol, 1)
    return my_sol

    raise NotImplementedError
