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


def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1

def remove_pentomino(board, pent_idx):
    board[board==pent_idx+1] = 0

def add_pentomino(board, pent, coord, check_pent=False, valid_pents=None):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the pent and coord[1] is the lowest
    column index.

    check_pent will also check if the pentomino is part of the valid pentominos.
    """
    if check_pent and not is_pentomino(pent, valid_pents):
        return False
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != 0: # Overlap
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True

# test if a board is complete i.e. all elements are non-zero
def goal_test(board):
    for row in board:
        for i in row:
            if i == 0:
                return False
    return True

# determine if a list contains a numpy array
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

def pent_equal(pent1, pent2):
    if pent1.shape == pent2.shape:
        for i in range(0,pent1.shape[0]):
            for j in range(0,pent1.shape[1]):
                if pent1[i][j] != pent2[i][j]:
                    return False
        return True
    return False

# recursive helper function for solve
def solve_r(board, pents, sol):
    if len(pents) == 0 or goal_test(board):
        return True
    init_pent = pents.pop()
    current_pent = init_pent
    if len(pents) == 0:
        cur_idx = get_pent_idx(current_pent)
        for k in range(0, len(translation_list[cur_idx])):
            cur_trans = translation_list[cur_idx][k]
            for i in range(0,board.shape[0] - cur_trans.shape[0] + 1):
                for j in range(0,board.shape[1] - cur_trans.shape[1] + 1):
                    if add_pentomino(board, cur_trans, (i,j)):
                        sol.append((cur_trans, (i,j)))
                        if board[i][j] != 0 and solve_r(board, pents, sol):
                            return True
                        remove_pentomino(board,cur_idx)
        pents.insert(0, current_pent)
        current_pent = pents.pop()
    else:
        while not pent_equal(pents[len(pents)-1], init_pent):
            cur_idx = get_pent_idx(current_pent)
            for k in range(0, len(translation_list[cur_idx])):
                cur_trans = translation_list[cur_idx][k]
                for i in range(0,board.shape[0] - cur_trans.shape[0] + 1):
                    for j in range(0,board.shape[1] - cur_trans.shape[1] + 1):
                        if add_pentomino(board, cur_trans, (i,j)):
                            sol.append((cur_trans, (i,j)))
                            if board[i][j] != 0 and solve_r(board, pents, sol):
                                return True
                            remove_pentomino(board,cur_idx)
            pents.insert(0, current_pent)
            current_pent = pents.pop()
    return False


def solve(board, pents, app=None):
    # our_board[i][j] is value in domino at that spot, 0 if unassigned
    our_board = np.zeros_like(board)
    my_sol = []

    # store list of all transformations in translation_list
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
        translation_list.append(trans_pent)

    our_pents = pents.copy()
    solve_r(our_board, our_pents, my_sol)
    if app is not None:
        app.draw_solution_and_sleep(my_sol, 1)
    print(my_sol)
    return my_sol

    raise NotImplementedError
