#Sahil Agrawal
#Set up the board
    #draw all squares (8x8 board)
    #Put four discs in the center of the board (squares (4,3) and (3,4) have black circles
        #squares (3,3) and (4,4) have white squares
    #create a message box
    #Allow the human to choose between playing Black and White

from OthelloGUIs import *
from SquareOthellov2 import *
from OthelloAI import *
from PieceOthello import *
from Button import Button
from graphics import *

def otherColor(color):
    if color == 'black':
        return 'white'
    else:
        return 'black'
    
def main():
    #set up board
    GUI = OthelloBoard()
    piece = Piece()

    #create AI object
    AIColor = GUI.returnAIColor()

    AI = OthelloAI(GUI.returnAIColor())


     # sets up the start of the game; black always goes first
    GUI.setGameStart("It is Black’s turn – please click a valid open square")
    gameOver = False
    turnNum = 0
    while not gameOver: # while the game is not over:
        for color in ["black","white"]:
            turnNum += 1
            #get all valid moves. This is needed for both the AI and the player
            GUI.updateMessage("It is "+color+"'s move")
            validMoves = piece.getPossibleMoves(GUI,color)
            if validMoves == []:
                #if no moves, then wait for user input
                #happens regardless of whose turn it is
                validMovesOpp = piece.getPossibleMoves(GUI, otherColor(color))
                if validMovesOpp == []:
                    gameOver = True
                
            #AI's turn

            elif color == AIColor:
                #it is the AI's turn
                #change layer (3rd parameter)
                GUI.setThinking()
                move = AI.chooseMove(GUI,piece,validMoves, turnNum)
                if move != []:
                    flippedPieces = piece.getFlippedPieces(move[0],move[1],GUI, color)
                    #flips the squares
                    GUI.updateBoard(move[0], move[1], flippedPieces,color)
                    GUI.highlight([move])
                    GUI.unsetThinking()
               
            else:
                GUI.highlight(validMoves)
                #user's turn and they have a valid move
                move = GUI.getClickedSquare()
                #check if the square the user clicked is in the list of valid moves
                while move not in validMoves:
                    move = GUI.getClickedSquare()
                    GUI.updateMessage("Click on a valid square")
                #after getting a valid move
                #update board (change flipped pieces)
                flippedPieces = piece.getFlippedPieces(move[0], move[1], GUI, color)
                GUI.updateBoard(move[0], move[1], flippedPieces, color)
                GUI.unhighlight(validMoves)
                
            #set winning conditions
            #checking if all the squares have been taken
            numBlack,numWhite,numBlank, = 0,0,0
            numBlack = len(GUI.getTeamSquares("black"))
            numWhite = len(GUI.getTeamSquares("white"))
            numBlank = 64 - numBlack - numWhite

            if (validMoves == []) and (not gameOver):
                GUI.waitForClick(message="No valid moves for current player. Click anywhere to proceed.")
                
            elif (numBlank != 0) and (not gameOver):
                GUI.waitForClick()
                if (color == AIColor) and (validMoves != []):
                    GUI.unhighlight([move])
                
            else:
                gameOver = True
                #determine who won
                if numWhite>numBlack:
                    GUI.setEndGame("white")
                    #white won

                elif numWhite<numBlack:
                    #black won
                    GUI.setEndGame("black")
                    
                else:
                    GUI.updateMessage("game is done.")

main()
