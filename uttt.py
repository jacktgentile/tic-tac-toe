from time import sleep
from math import inf
from random import randint
import copy
class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

        self.bestOption = (-1, -1)

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def ofThreeAtLeastTwo(self, val1, val2, val3, isMax):
        ct = 0;
        if isMax:
            if val1 == self.maxPlayer:
                ct += 1
            elif val1 == self.minPlayer:
                ct -= 1
            if val2 == self.maxPlayer:
                ct += 1
            elif val2 == self.minPlayer:
                ct -= 1
            if val3 == self.maxPlayer:
                ct += 1
            elif val3 == self.minPlayer:
                ct -= 1
            return ct >= 2

        else:
            if val1 == self.maxPlayer:
                ct -= 1
            elif val1 == self.minPlayer:
                ct += 1
            if val2 == self.maxPlayer:
                ct -= 1
            elif val2 == self.minPlayer:
                ct += 1
            if val3 == self.maxPlayer:
                ct -= 1
            elif val3 == self.minPlayer:
                ct += 1
            return ct >= 2

    def countUnblockedTwoLocal(self, startIdx, isMax):
        x = startIdx[0]
        y = startIdx[1]
        ct = 0
        if self.ofThreeAtLeastTwo(self.board[0 + x][0 + y], self.board[1 + x][1 + y], self.board[2 + x][2 + y], isMax):
            ct += 1
        if self.ofThreeAtLeastTwo(self.board[2 + x][0 + y], self.board[1 + x][1 + y], self.board[0 + x][2 + y], isMax):
            ct += 1
        # check rows going down
        for i in range(3):
            if self.ofThreeAtLeastTwo(self.board[0 + i + x][0 + y], self.board[0 + i + x][1 + y], self.board[0 + i + x][2 + y], isMax):
                ct += 1
        # check columns going left to right
        for i in range(3):
            if self.ofThreeAtLeastTwo(self.board[0 + x][0 + i + y], self.board[1 + x][0 + i + y], self.board[2 + x][0 + i + y], isMax):
                ct += 1
        return ct


    def countUnblockedTwo(self, isMax):
        # number of unblocked 2 in a rows
        ct = 0
        for curr_start in self.globalIdx:
            ct += self.countUnblockedTwoLocal(curr_start, isMax)
        return ct


    def blocked(self, val1, val2, val3, isMax):
        if isMax:
            group = [val1, val2, val3]
            group.sort()
            comp = ['O', 'X', 'X']
            if (group == comp):
                return True
            else:
                return False
        else:
            group = [val1, val2, val3]
            group.sort()
            comp = ['O', 'O', 'X']
            if (group == comp):
                return True
            else:
                return False

    def countBlockedOpponentLocal(self, startIdx, isMax):
        x = startIdx[0]
        y = startIdx[1]
        ct = 0
        if self.blocked(self.board[0 + x][0 + y], self.board[1 + x][1 + y], self.board[2 + x][2 + y], isMax):
            ct += 1
        if self.blocked(self.board[2 + x][0 + y], self.board[1 + x][1 + y], self.board[0 + x][2 + y], isMax):
            ct += 1
        # check rows going down
        for i in range(3):
            if self.blocked(self.board[0 + i + x][0 + y], self.board[0 + i + x][1 + y], self.board[0 + i + x][2 + y], isMax):
                ct += 1
        # check columns going left to right
        for i in range(3):
            if self.blocked(self.board[0 + x][0 + i + y], self.board[1 + x][0 + i + y], self.board[2 + x][0 + i + y], isMax):
                ct += 1
        return ct

    def countBlockedOpponent(self, isMax):
        # number of times curr player has blocked opponent
        ct = 0
        for curr_start in self.globalIdx:
            ct += self.countBlockedOpponentLocal(curr_start, isMax)
        return ct

    def countCornersLocal(self, startIdx, isMax):
        x = startIdx[0]
        y = startIdx[1]
        if isMax:
            ct = 0
            if (self.board[0 + x][0 + y] == self.maxPlayer):
                ct += 1
            if (self.board[2 + x][0 + y] == self.maxPlayer):
                ct += 1
            if (self.board[0 + x][2 + y] == self.maxPlayer):
                ct += 1
            if (self.board[2 + x][2 + y] == self.maxPlayer):
                ct += 1
            return ct
        else:
            ct = 0
            if (self.board[0 + x][0 + y] == self.minPlayer):
                ct += 1
            if (self.board[2 + x][0 + y] == self.minPlayer):
                ct += 1
            if (self.board[0 + x][2 + y] == self.minPlayer):
                ct += 1
            if (self.board[2 + x][2 + y] == self.minPlayer):
                ct += 1
            return ct

    def countCorners(self, isMax):
        ct = 0
        for curr_start in self.globalIdx:
            ct += self.countCornersLocal(curr_start, isMax)
        return ct

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0.0
        if isMax:
            # rule1
            if self.checkWinner() == 1: # max wins!
                # print("util", 10000)
                return 10000
            # rule2
            res = self.countUnblockedTwo(isMax) 
            if res > 0:
                score += res * 500
            res = self.countBlockedOpponent(isMax)
            if res > 0:
                score += res * 100
            if score > 0:
                # print("util = ", score)
                return score
            # rule3
            res = self.countCorners(isMax)
            # print("util = ", res * 30)
            return res * 30
        else:
            # rule1
            if self.checkWinner() == -1: # min wins!
                # print("util = ", -10000)
                return -10000

            # rule2
            res = self.countUnblockedTwo(isMax) 
            if res > 0:
                score -= res * 500
            res = self.countBlockedOpponent(isMax)
            if res > 0:
                score -= res * 100
            if score > 0:
                # print("util = ", score)
                return score

            # rule3
            res = self.countCorners(isMax)
            # print("util = ", res * -30)
            return res * -30


    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for row in self.board:
            if '_' in row:
                return True
        return False

    def checkLocalBoard(self, startIdx):
        # print("checking local", startIdx)
        x = startIdx[0]
        y = startIdx[1]
        if self.board[0 + x][0 + y] == self.board[1 + x][1 + y] == self.board[2 + x][2 + y] != '_': # diag win
            if self.board[0 + x][0 + y] == self.maxPlayer:
                return 1
            elif self.board[0 + x][0 + y] == self.minPlayer:
                return -1
        if self.board[0 + x][2 + y] == self.board[1 + x][1 + y] == self.board[2 + x][0 + y] != '_': # other diag win
            if self.board[0 + x][2 + y] == self.maxPlayer:
                return 1
            elif self.board[0 + x][2 + y] == self.minPlayer:
                return -1
        # check rows going down
        for i in range(3):
            if self.board[0 + i + x][0 + y] == self.board[0 + i + x][1 + y] == self.board[0 + i + x][2 + y] != '_':
                if self.board[0 + i + x][0 + y] == self.maxPlayer:
                    return 1
                elif self.board[0 + i + x][0 + y] == self.minPlayer:
                    return -1
        # check columns going left to right
        for i in range(3):
            if self.board[0 + x][0 + i + y] == self.board[1 + x][0 + i + y] == self.board[2 + x][0 + i + y] != '_':
                if self.board[0 + x][0 + i + y] == self.maxPlayer:
                    return 1
                elif self.board[0 + x][0 + i + y] == self.minPlayer:
                    return -1
        return 0 # no winner yet in local board

    def checkWinner(self):
        #Return terminal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        for curr_start in self.globalIdx:
            res = self.checkLocalBoard(curr_start) # 1, -1, or 0
            if res != 0: # found a winner!
                return res
        return 0 # no winner yet

    def emptyCells(self, startIdx):
        # returns empty cell coordinates relative to whole board, given local starting pt
        '''
        for example if board is
        O _ X   O O X   O X _
        _ X _   _ X _   _ _ _
        X _ _   _ X O   _ _ _

        _ _ _   X _ O   _ _ _
        _ _ _   _ _ _   _ _ _
        _ _ _   _ _ _   _ _ _

        _ _ _   _ _ _   _ _ _
        _ _ _   _ _ _   _ _ _
        _ _ _   _ _ _   _ _ _
        and emptyCells(self, startIdx = (0, 4)) is called, we look at top center local board
        should return [(1,4), (2,4), (1, 6)]
        '''
        empties = []
        x = startIdx[0]
        y = startIdx[1]
        for i in range(3):
            for j in range(3):
                if self.board[i + x][j + y] == '_':
                    empties.append((i + x, j + y))
        return empties

    def newCurrBoardIdx(self, cell, startIdx):
        # cell should be relative to whole board, not local
        x = cell[0] - startIdx[0]
        y = cell[1] - startIdx[1]
        # print("cell is", cell)
        # print("startIdx is", startIdx)
        if x == 0:
            if y == 0:
                return 0
            if y == 1:
                return 1
            if y == 2:
                return 2
        if x == 1:
            if y == 0:
                return 3
            if y == 1:
                return 4
            if y == 2:
                return 5
        if x == 2:
            if y == 0:
                return 6
            if y == 1:
                return 7
            if y == 2:
                return 8
        raise ValueError("values in cell/startIdx in correct!") # for debugging, remove for submission
        return -1 # something went wrong!

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE


        score=0.0

        if isMax:
            if depth >= 3 or self.checkWinner() != 0:
                return self.evaluatePredifined(isMax)
            score = -inf
            empties = self.emptyCells(self.globalIdx[currBoardIdx])
            for cell in empties:
                x, y = cell[0], cell[1]
                self.board[x][y] = self.maxPlayer
                newCBI = self.newCurrBoardIdx(cell, self.globalIdx[currBoardIdx])
                score = max(score, self.alphabeta(depth + 1, newCBI, alpha, beta, not isMax))
                self.board[x][y] = '_'
                if score >= beta: # stop searching
                    return score
                alpha = max(alpha, score)
            return score
        else:
            if depth >= 3 or self.checkWinner() != 0:
                return self.evaluatePredifined(isMax)
            score = inf
            empties = self.emptyCells(self.globalIdx[currBoardIdx])
            for cell in empties:
                x, y = cell[0], cell[1]
                self.board[x][y] = self.maxPlayer
                newCBI = self.newCurrBoardIdx(cell, self.globalIdx[currBoardIdx])
                score = min(score, self.alphabeta(depth + 1, newCBI, alpha, beta, not isMax))
                self.board[x][y] = '_'
                if score <= alpha:
                    return score
                beta = min(beta, score)
            return score

        return score

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        bestValue=0.0
        self.expandedNodes += 1

        if isMax:
            bestValue = -inf
            beop = (-1,-1)
            if depth >= 3 or self.checkWinner() != 0: # base case
                # if self.checkWinner() != 0:
                #     print("at depth", depth, "found winner")
                #     self.printGameBoard()
                return self.evaluatePredifined(isMax)

            empties = self.emptyCells(self.globalIdx[currBoardIdx])
            for cell in empties:
                x, y = cell[0], cell[1]
                self.board[x][y] = self.maxPlayer
                newCBI = self.newCurrBoardIdx(cell, self.globalIdx[currBoardIdx])
                score = self.minimax(depth + 1, newCBI, not isMax)
                self.board[x][y] = '_' # revert back
                if score > bestValue:
                    bestValue = score
                    beop = cell # just added this
            self.bestOption = beop
            return bestValue
        else:
            bestValue = inf
            beop = (-1, -1)
            if depth == self.maxDepth or self.checkWinner() != 0: # base case
                return self.evaluatePredifined(isMax)

            empties = self.emptyCells(self.globalIdx[currBoardIdx])
            for cell in empties:
                x, y = cell[0], cell[1]
                self.board[x][y] = self.minPlayer
                newCBI = self.newCurrBoardIdx(cell, self.globalIdx[currBoardIdx])
                score = self.minimax(depth + 1, newCBI, not isMax)
                self.board[x][y] = '_' # revert back
                if score < bestValue:
                    bestValue = score
                    beop = cell # just added this
            self.bestOption = beop
            return bestValue


    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes=[]
        winner=0

        #TODO: make this work, as of now score is not positive when isMax


        currBoardIdx = self.startBoardIdx

        if not isMinimaxOffensive and not isMinimaxDefensive:
            isMax = maxFirst
            while True:
                empties = self.emptyCells(self.globalIdx[currBoardIdx])
                best = 0
                if isMax:
                    best = -inf
                else:
                    best = inf
                bestCell = (-1, -1)
                bestCBI = -1
                for cell in empties: # tuples
                    self.expandedNodes += 1
                    if isMax:
                        self.board[cell[0]][cell[1]] = self.maxPlayer
                    else:
                        self.board[cell[0]][cell[1]] = self.minPlayer
                    newCBI = self.newCurrBoardIdx(cell, self.globalIdx[currBoardIdx])
                    score = self.alphabeta(1, newCBI, -inf, inf, not isMax)
                    self.board[cell[0]][cell[1]] = '_'
                    if (isMax and score > best):
                        best = score
                        bestCell = cell
                        bestCBI = newCBI
                    elif (not isMax and score < best):
                        best = score
                        bestCell = cell
                        bestCBI = newCBI
                bestValue.append(best)
                bestMove.append(bestCell)
                expandedNodes.append(self.expandedNodes) # num nodes expanded 
                self.expandedNodes = 0;
                currBoardIdx = bestCBI
                if isMax:
                    self.board[bestCell[0]][bestCell[1]] = self.maxPlayer
                else:
                    self.board[bestCell[0]][bestCell[1]] = self.minPlayer
                gameBoards.append(copy.deepcopy(self.board))
                isMax = not isMax
                # break if found winner
                res = self.checkWinner()
                # self.printGameBoard()  
                if res != 0:
                    winner = res
                    break


        elif isMinimaxOffensive and isMinimaxDefensive:
            isMax = maxFirst
            while True:
                empties = self.emptyCells(self.globalIdx[currBoardIdx])
                best = 0
                if isMax:
                    best = -inf
                else:
                    best = inf
                bestCell = (-1, -1)
                bestCBI = -1
                for cell in empties: # tuples
                    self.expandedNodes += 1
                    if isMax:
                        self.board[cell[0]][cell[1]] = self.maxPlayer
                    else:
                        self.board[cell[0]][cell[1]] = self.minPlayer
                    newCBI = self.newCurrBoardIdx(cell, self.globalIdx[currBoardIdx])
                    score = self.minimax(1, newCBI, not isMax)
                    self.board[cell[0]][cell[1]] = '_'
                    if (isMax and score > best):
                        best = score
                        bestCell = cell
                        bestCBI = newCBI
                    elif (not isMax and score < best):
                        best = score
                        bestCell = cell
                        bestCBI = newCBI
                bestValue.append(best)
                bestMove.append(bestCell)
                expandedNodes.append(self.expandedNodes) # num nodes expanded 
                self.expandedNodes = 0;
                currBoardIdx = bestCBI
                if isMax:
                    self.board[bestCell[0]][bestCell[1]] = self.maxPlayer
                else:
                    self.board[bestCell[0]][bestCell[1]] = self.minPlayer
                gameBoards.append(copy.deepcopy(self.board))
                isMax = not isMax
                # break if found winner
                res = self.checkWinner()
                # self.printGameBoard()  
                if res != 0:
                    winner = res
                    break

        
        # if isMinimaxOffensive and isMinimaxDefensive:
        #     currBoardIdx = self.startBoardIdx
        #     isMax = maxFirst
        #     while True:
        #         currScore = self.minimax(1, currBoardIdx, isMax)
        #         takeMove  = self.bestOption # bestOption updated in minimax
        #         bestValue.append(currScore)
        #         bestMove.append(takeMove)
        #         expandedNodes.append(self.expandedNodes) # num nodes expanded 
        #         self.expandedNodes = 0
        #         if isMax:
        #             self.board[takeMove[0]][takeMove[1]] = self.maxPlayer
        #         else:
        #             self.board[takeMove[0]][takeMove[1]] = self.minPlayer
        #         self.printGameBoard()
        #         currBoardIdx = self.newCurrBoardIdx(takeMove, self.globalIdx[currBoardIdx])
        #         isMax = not isMax # flip for next player 
        #         res = self.checkWinner()
        #         if res != 0:
        #             winner = res
        #             break

        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
