# Piece class

from graphics import *
from SquareOthellov2 import *

class Piece:
    """Each Piece is circular shaped in either black or white color."""
    def __init__(self):
        self.eaten = False
        self.numSpaces = 8
        self.listDir= [[0,1],[1,0],[0,-1],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]


    def getPossibleMoves(self,gui,color):
        "This method finds all possible spots."
        self.spots =[]
        squaresList = gui.returnSquares() # returns all the squares on the board
        
        opponentColor = ''
            
        if color == 'white':
            opponentColor = 'black'
        elif color == 'black':
            opponentColor = 'white'
    
        for sq in squaresList: # goes through each square on the board
            if not sq.returnOccupied(): # if the square is not occupied:
                x, y = int(sq.getX()), int(sq.getY()) # gets x and y coordinates of square
                for direction in self.listDir: # goes through each direction
                    for i in range(1, self.numSpaces): # goes through each space in each direction
                        if (x + i*direction[0] < self.numSpaces) and (x + i*direction[0] >= 0) and (y + i*direction[1] >= 0) and (y + i*direction[1] < self.numSpaces):
                            square = gui.getSquare(x + i*direction[0], y + i*direction[1])
                            # checks if adjacent square in this direction belongs to opponent
                            if (square.getColor() != opponentColor) and (i == 1):
                                # if it doesn't, then it skips this direction
                                break
                            # the adjacent square is occupied by opponent, check if there is a chain of opponent squares
                            if (square.getColor() == ''): # checks if there is a break in the chain
                                break
                                # check if player's piece is at the end
                            if (square.getColor() == color) and (i != 1): # if there is, then "sq" is a possible square                            
                                self.spots.append([sq.getX(), sq.getY()])
                                break      

        return self.spots
                        
    def getFlippedPieces(self,x,y,gui, color):
        "Returns what pieces would be flipped after a valid move."
        # similar approach to getPossibleMoves, but this method returns flipped squares instead of possible squares
        flippedSquares = []
        opponentColor = ''
        if color == 'white':
            opponentColor = 'black'
        elif color == 'black':
            opponentColor = 'white'
        #print(opponentColor)
        #newSquare = gui.getSquare(x,y)
        #print(newSquare.getX(),newSquare.getY())
        for direction in self.listDir:
            for i in range(1, self.numSpaces):
                if (x + i*direction[0] < self.numSpaces) and (x + i*direction[0] >= 0) and (y + i*direction[1] >= 0) and (y + i*direction[1] < self.numSpaces):
                    square = gui.getSquare((x + i*direction[0]), (y + i*direction[1]))
                    # checks if adjacent square in this direction belongs to opponent
                    if (square.getColor() != opponentColor) and (i == 1):
                        # if it doesn't, then it skips this direction
                        break
                    # the adjacent square is occupied by opponent, check if there is a chain of opponent squares
                    if (square.getColor() == ''):
                        break
                        # check if player's piece is at the end
                    if (square.getColor() == color) and (i != 1): # if there is, then go through and get the flipped squares
                        for t in range(i): # gets all the flipped squares
                            flippedSquares.append(gui.getSquare(x + t*direction[0],y + t*direction[1]))
                        break      
               

        return flippedSquares
