#Sahil Agrawal
#OthelloAI.py
'''
The AI is given a set of possible valid moves where it can place a piece. If it has multiple options for the move,
then it intelligently picks among them via a utility function. Given valid move A, we internally simulate the AI
placing a piece of its color at location A. Then, we calculate statistics based on the simulation separately per team (AI and user):
sum of "weights" for pieces on the board, number of corners occupied, number of squares adjacent to the corner occupied and whether those squares
are advantageous or disadvantageous, number of valid moves, and number of pieces held by that team's color. We calculate a score for that valid move
by a utility function like: weight1 * (AIstatistic1 - userStatistic1) + ... . Weights are set based on the importance of the different statistics,
and the statistics hold different degrees of importance at different times in the game. The AI chooses the valid move with the maximum calculated score.
'''
import random
from OthelloWeightedBoard import *

class OthelloAI:

    def __init__(self, color):
        self.color = color
        
        if self.color == "black":
            self.userColor = "white"
        else:
            self.userColor = "black"
            
        self.weightedBoard = WeightedBoard()
    
    def getClosestCorner(self, x, y):
        if [x, y] in [[0,1],[1,0],[1,1]]: return [0,0]
        elif [x,y] in [[6,0],[7,1],[6,1]]: return [7,0]
        elif [x,y] in [[1,7],[0,6],[1,6]]: return [0,7]
        else: return [7,7]

    def checkNextCorner(self, corner, AIpieces, GUI, myColor, addWeightPos, addWeightNeg):

        #Checks whether the spots adjacent to corners are advantageous or disadvantageous for our team
        x,y = corner[0], corner[1]
        cornerSq = GUI.getSquare(corner[0], corner[1])
        posNextCorner, negNextCorner = 0, 0

        if cornerSq.returnOccupied():
            #advantageous to occupy position next to corner if the corner is already held by our team, because then less likely to flip
            if cornerSq.getColor() == myColor:
                posNextCorner += 1
                self.weightedBoard.addWeight(x, y, addWeightPos)
        else:
            #bad to occupy position next to corner if corner is not occupied
            negNextCorner += 1
            self.weightedBoard.addWeight(x, y, addWeightNeg)

        return posNextCorner, negNextCorner

    def teamHeuristics(self, GUI, teamPieces, color):

        statsDict = {"weightPoints":0, "numCorners":0,
                     "numPosAdjCorner":0, "numNegAdjCorner":0, "numPosDiagCorner":0,
                     "numNegDiagCorner":0, "color":color}

        for sq in teamPieces:
            x, y = sq.getLocation()
            
            if [x, y] in [[0,0], [0,7], [7,0], [7,7]]:
                statsDict["numCorners"] += 1

            #diagonal next to corner: get similar statistic depending on who is in the corner
            #how many advantageous and disadvantegous "diagonal next to corner" squares does our team occupy?
            if self.weightedBoard.getWeight(x, y) == -20:
                corner = self.getClosestCorner(x, y)
                posDiagCorner, negDiagCorner = self.checkNextCorner(corner, teamPieces, GUI, color, 40, -20)
                statsDict["numPosDiagCorner"] += posDiagCorner
                statsDict["numNegDiagCorner"] += negDiagCorner
                
            #edge adjacent to corner: could be particularly good or bad depending on who is in the corner
            #how many advantageous and disadvantegous "edge next to corner" squares does our team occupy?
            if self.weightedBoard.getWeight(x, y) == -10:
                corner = self.getClosestCorner(x, y)
                posAdjCorner, negAdjCorner = self.checkNextCorner(corner, teamPieces, GUI, color, 50, -30)
                statsDict["numPosAdjCorner"] += posAdjCorner
                statsDict["numNegAdjCorner"] += negAdjCorner

            statsDict["weightPoints"] += self.weightedBoard.getWeight(x,y)

            self.weightedBoard.reset()
            
        return statsDict
                
    def applyHeuristics(self, GUI, pieces, myColor, oppColor, turnNum):

        #function to get squares of the desired color
        AIpieces = GUI.getTeamSquares(myColor)
        oppPieces = GUI.getTeamSquares(oppColor)
        squaresList = GUI.returnSquares()

        #get statsDict for AI and opponent separately because we want the move to maximize the AI utility
        #and minimize the opponent utility. 
        statsDictAI = self.teamHeuristics(GUI, AIpieces, myColor)
        statsDictAI["numPieces"] = len(AIpieces)
        statsDictOpp = self.teamHeuristics(GUI, oppPieces, oppColor)
        statsDictOpp["numPieces"] = len(oppPieces)

        for statsDict in [statsDictAI, statsDictOpp]:
            #relevant b/c if it's better to maximize AI's number of valid moves (i.e. mobility)
            #and minimize opponent's number of valid moves
            statsDict["numValidMoves"] = len(pieces.getPossibleMoves(GUI, statsDict["color"]))

        #beginning of the game
        if turnNum < 12:
            statsWeight = {"weightPoints":45, "numCorners":18000,
                     "numPosAdjCorner":2500, "numNegAdjCorner":-2300, "numPosDiagCorner":600,
                     "numNegDiagCorner":-700, "numValidMoves": 50, "numPieces":3}

        #middle of the game
        elif turnNum < 50:
            statsWeight = {"weightPoints":30, "numCorners":19000,
                     "numPosAdjCorner":2700, "numNegAdjCorner":-2300, "numPosDiagCorner":650,
                     "numNegDiagCorner":-750, "numValidMoves": 70, "numPieces":3}

        #end of the game, become greedier so numPieces weight goes up
        else:
            statsWeight = {"weightPoints":20, "numCorners":12000,
                     "numPosAdjCorner":1200, "numNegAdjCorner":-1900, "numPosDiagCorner":600,
                     "numNegDiagCorner":-720, "numValidMoves": 100, "numPieces":100}
            
        moveScore = 0
        for key in statsDictAI.keys():
            if key != "color":
                if key in ["numValidMoves", "numPieces"]:
                    #normalize to be a value between 1 and 100
                    if (statsDictAI[key] != 0) or (statsDictOpp[key] != 0):
                        moveScore += statsWeight[key] * (100 * (statsDictAI[key] - statsDictOpp[key]) / (statsDictAI[key] + statsDictOpp[key]))

                else:
                    moveScore += statsWeight[key] * ((statsDictAI[key] - statsDictOpp[key])) 

        return moveScore
                
    #validMoves is a list of [x, y] coordinates
    #assuming that [x, y] are 0-7
    def chooseMove(self, GUI, pieces, validMoves, turnNum):

        #if no valid moves, return nothing
        if len(validMoves) == 0: 
            return []

        #if only one valid move, return that
        elif len(validMoves) == 1:
            return validMoves[0]

        #multiple valid moves
        #list of utlity function scores for each move in validMoves list
        scoreList = []

        for move in validMoves:
                
            #Simulate the AI moving to that location on the board
            #Images should not be updated, and no win/lose messaging should occur
            GUI.fakeMove(move[0], move[1], pieces.getFlippedPieces(move[0], move[1], GUI, self.color), self.color)
            score = self.applyHeuristics(GUI, pieces, self.color, self.userColor, turnNum)                
            scoreList.append(score)

            #undo the simulated move
            GUI.undoFakeMove()

        maxScore = max(scoreList)

        
        #find all indices of the maximum score and pick randomly if multiple best options
        indices = []
        for i in range(len(scoreList)):
            if scoreList[i] == maxScore:
                indices.append(i)

        moveInd = random.choice(indices)

        return validMoves[moveInd]
