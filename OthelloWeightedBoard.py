#Sahil Agrawal
#Weighted board sets a static weight for each position on the board
#depending on whether that position is generally advantageous or disadvantageous to hold.
#The corners are generally the best spots on the board to take,
#because they cannot be flipped, so they are given the score 100.
#Spots adjacent to the corner are generally disadvantageous to take (with exceptions)
#because they may enable the opponent to take the corner.

class WeightedBoard:
    
    def __init__(self):
        self.boardWeights = [[100, -10, 11, 6, 6, 11, -10, 100],
                         [-10, -20, 1, 2, 2, 1, -20, -10],
                         [10, 1, 5, 4, 4, 5, 1, 10],
                         [6, 2, 4, 2, 2, 4, 2, 6],
                         [6, 2, 4, 2, 2, 4, 2, 6],
                         [10, 1, 5, 4, 4, 5, 1, 10],
                         [-10, -20, 1, 2, 2, 1, -20, -10],
                         [100, -10, 11, 6, 6, 11, -10, 100]]

        #we can adjust dynamic board weights in a given turn if
        #there are exceptions (something that is normally disadvantegeous
        #is not in this case)
        self.dynamicBoard = [[100, -10, 11, 6, 6, 11, -10, 100],
                         [-10, -20, 1, 2, 2, 1, -20, -10],
                         [10, 1, 5, 4, 4, 5, 1, 10],
                         [6, 2, 4, 2, 2, 4, 2, 6],
                         [6, 2, 4, 2, 2, 4, 2, 6],
                         [10, 1, 5, 4, 4, 5, 1, 10],
                         [-10, -20, 1, 2, 2, 1, -20, -10],
                         [100, -10, 11, 6, 6, 11, -10, 100]]
        
        self.minBoardWeight = -20

    def getWeight(self, x, y):
        return self.dynamicBoard[int(y)][int(x)]

    def addWeight(self, x, y, incWeight):
        self.dynamicBoard[int(y)][int(x)] += incWeight

    def reset(self):
        self.dynamicBoard = self.boardWeights.copy()

    def sumAllWeights(self):
        boardSum = 0
        for i in range(8):
            boardSum += sum(self.boardWeights[i])
        return boardSum
