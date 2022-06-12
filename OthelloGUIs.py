# GUI class

from graphics import *
from SquareOthellov2 import *
from Button import *

class OthelloBoard:
    """Draws the GUI on which the Othello game can be played.
    The squares on the Othello board are buttons that the user
    clicks on to move the pieces."""

    def __init__(self):
        self.win = GraphWin("Othello Board", 1000,900)
        # setting coordinates
        self.win.setCoords(-2,-2,15,15)
        #self.win.setCoords(-2,15,15,-2)
        self.quit = False
        self.AIColor = ''

        self.msgBox = Text(Point(5,8.5), "Would you like to play as black or white?")
        self.msgBox.draw(self.win)
        self.msgBox2 = Text(Point(5,8.4),'')
        self.msgBox2.draw(self.win)

        # drawing the squares
        #Square(self.win,Point(1,1),1,1)
        #make a list of lists
        self.squaresList = []
        self.sWidth, self.sHeight = 1, 1
        self.squaresList = [ [], [], [], [], [], [], [], [] ]
        for row in range(7, -1, -1):
            for col in range(8):
                self.squaresList[row].append(Square(self.win, Point(col, row), self.sWidth, self.sHeight))

        self.xMin = -self.sWidth/2
        self.xMax = 7 + self.sWidth/2
        self.yMin = -self.sHeight/2
        self.yMax = 7+ self.sHeight/2

        # draws first four pieces on the board
        self.squaresList[3][3].setColor('black') 
        self.squaresList[4][3].setColor('white') 
        self.squaresList[3][4].setColor('white') 
        self.squaresList[4][4].setColor('black')

        # buttons for user to choose whether to play as black or white
        self.buttonBlack = Button(self.win,Point(8.5,5.5),1,2,"Black")
        self.buttonBlack.activate()
        self.buttonWhite = Button(self.win,Point(10.5,5.5),1,2,"White")
        self.buttonWhite.activate()

        pt = self.win.getMouse()
        while not (self.buttonBlack.clicked(pt) or self.buttonWhite.clicked(pt)):
            pt = self.win.getMouse()

        if self.buttonBlack.clicked(pt):
            self.userColor = "black"
            self.AIColor = "white"
        else:
            self.userColor = "white"
            self.AIColor = "black"

        self.buttonQuit = Button(self.win, Point(9,9.5), 1.5,0.7, "Quit")

        # all this below is for rank and file
        letterDict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}
        numbersDict = {0:'1',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',7:'8'}

        for i in range(0,8):
            number = numbersDict[i]
            Text(Point(-0.7,i),number).draw(self.win)
            letter = letterDict[i]
            Text(Point(i,7.7),letter).draw(self.win)

        

    def waitForClick(self, message="Click anywhere to proceed."):
        self.updateMessage(message)
        pt = self.win.getMouse()
        if (self.buttonQuit.clicked(pt)):
            self.quit = True

        return self.quit

    #row=y, col=x
    def getRow(self, x, y):
        return int(y)

    def getCol(self, x, y):
        return int(x)

    def undrawAsk(self):
        "Undraws the color ask and the entry box."
        self.colorAsk.undraw()
        self.entry.undraw()

    def getWin(self):
        "Returns the window of the GUI."
        return self.win

    def setGameStart(self, message):
        "Sets the starting conditions of the GUI."
        self.msgBox.undraw()
        self.msgBox = Text(Point(5,9.5), message)
        self.msgBox.draw(self.win)
        self.buttonQuit.activate()
        self.quit = False
        
    def updateMessage(self, message):
        "Prints messages to the GUI."
        self.msgBox.setText(message)

    def quitGame(self):
        "Quits the game and closes the GUI."
        self.win.close()
        sys.exit()

    
    def returnAIColor(self):
        "Returns the color the AI would be based on user input."
        
        return self.AIColor

    def isClickedOn8x8(self, p):
        "Determines if the user clicked on the board or not; returns True or False."
        if (p.getX() >= self.xMin and p.getX() <= self.xMax) and (p.getY() >= self.yMin and p.getY() <= self.yMax):
            return True
        else:
            return False
        
    def getQuitStatus(self):
        "Returns if self.quit is True or False."
        return self.quit

    def highlight(self, moves):
        "Accesses square class to highlight squares for possible moves user can make."
        for move in moves:
            self.squaresList[int(move[1])][int(move[0])].highlight()

    def unhighlight(self, moves):
        "Accesses square class to unhighlight squares."
        for move in moves:
            self.squaresList[int(move[1])][int(move[0])].unhighlight()

    def getClickedSquare(self):
        "Returns the square that was clicked on the board."
        p = self.win.getMouse()
        for row in range(8):
            for col in range(8):
                sq = self.squaresList[row][col]
                if sq.clicked(p) == True:
                    return [sq.getX(),sq.getY()]

    def returnSquares(self):
        "Returns a list of all the squares on the board."
        singleList = []
        for ele in self.squaresList:
            singleList.extend(ele)
        return singleList

    def allSquaresOccupiedCheck(self):
        "Checks if all the squares on the board are occupied, so that the game can end."
        occupiedList = []
        for row in range(8):
            for col in range(8):
                sq = self.squaresList[row][col]
                if sq.returnOccupied == True:
                    occupiedList.append('x')
                    
        if len(occupiedList) == 64:
            return True

    def updateBoard(self,moveX,moveY,flippedPieces,color):
        "Updates the board after each move."
        self.squaresList[self.getRow(moveX,moveY)][self.getCol(moveX,moveY)].setColor(color)
        for piece in flippedPieces:
            x,y = int(piece.getX()), int(piece.getY())
            self.squaresList[self.getRow(x,y)][self.getCol(x,y)].setColor(color)
            

    def getMouse(self):
        "Gets mouse clicks."
        pt = self.win.getMouse()
        return pt

    def getSquare(self, x,y):
        "Gets square based on x and y coordinates."
        return self.squaresList[int(self.getRow(x,y))][int(self.getCol(x,y))]

    def fakeMove(self, moveX, moveY,flippedPieces,color):
        "Fake move for AI."
        self.fakeMoves = []
        self.squaresList[self.getRow(moveX,moveY)][self.getCol(moveX,moveY)].setFakeColor(color)
        for piece in flippedPieces:
            x,y = int(piece.getX()), int(piece.getY())
            self.squaresList[y][x].setFakeColor(color)
            self.fakeMoves.append([x,y])
        self.fakeMoves.append([moveX,moveY])

    def undoFakeMove(self):
        "Undos fake move."
        for move in self.fakeMoves:
            self.squaresList[int(move[1])][int(move[0])].undoFakeColor()
        self.fakeMoves = []

    def getTeamSquares(self, color):
        "Gets squares of the same color."
        colorLst = []
        for row in range(8):
            for col in range(8):
                sq = self.squaresList[row][col]
                if sq.getColor() == color:
                    colorLst.append(sq)

        return colorLst

    def setEndGame(self,color):
        self.msgBox.setText(color+ " has won the game. Click quit button to exit.")
        pt = self.win.getMouse()
        while not self.buttonQuit.clicked(pt):
            pt = self.win.getMouse()
        self.quit = True
        self.quitGame()
    
    def setThinking(self):
        "Thinking text for AI."
        self.msgBox2.setText('Thinking...')

    def unsetThinking(self):
        "Undraws Thinking text."
        self.msgBox2.setText('')
