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

def solve(board, pents, app=None):
    my_sol = []
    if app is not None:
        app.draw_solution_and_sleep(my_sol, 1)
    return my_sol

    raise NotImplementedError
