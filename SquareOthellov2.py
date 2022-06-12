# This is the Square subclass of superclass Button that represents each
#   square of the Othello board.

from Button import *
from graphics import *

class Square(Button):
    def __init__(self,win,center,width,height):
        """Initializes the square with instance variables including
            dimension, point, window, color, and active."""
        w,h=width/2.0,height/2.0
        x,y=center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        self.p1=Point(self.xmin, self.ymin)
        self.p2=Point(self.xmax, self.ymax)
        self.rect=Rectangle(self.p1,self.p2)
        self.win = win
        self.width = width

        self.rect.setFill('green3')
        self.rect.draw(win)
        self.center = center
        self.active = False
        self.occupied = False
        self.pieceColor = ''
        self.pieceRealColor = ''

    #Not Needed
    def activate(self):
        """Activates the square visually and sets boolean to True."""
        self.rect.setFill("red")
        self.rect.setWidth(2)
        self.active = True

    #Not Needed
    def deactivate(self):
        """Deactivates the square visually and sets boolean to False."""
        self.rect.setFill(self.color)
        self.rect.setWidth(1)
        self.active = False

    def setOccupied(self):
        """Returns the boolean status of occupied."""
        self.occupied = True

    def setColor(self,color):
        '''Draws a circle (the piece) on the square, given the color of the piece'''
        self.occupied = True
        self.pieceColor = color
        self.pieceRealColor = color
        self.circle=Circle(self.center,self.width-0.6)
        self.circle.setFill(color)
##        self.circle.setOutline("black")
##        self.circle.setWidth(5)
        self.circle.draw(self.win)

    def setFakeColor(self,color):
        self.pieceColor = color

    def undoFakeColor(self):
        self.pieceColor = self.pieceRealColor
        
    def getLocation(self):
        """Returns two values, x and y."""
        return self.center.getX(),self.center.getY()
    def getX(self):
        '''Returns x value of center'''
        return self.center.getX()
    def getY(self):
        '''Returns y value of center'''
        return self.center.getY()

    #Not needed
    def checkActive(self):
        """Returns the active boolean for squares."""
        return self.active

    def returnOccupied(self):
        return self.occupied

    def getType(self):
        """Returns the type of the square."""
        return self.type

    def getColor(self):
        """Returns the color of the square. Note that this could be a color for a fake move."""
        return self.pieceColor

    def highlight(self):
        "Highlights square."
        self.rect.setFill('green yellow')

    def unhighlight(self):
        "Unhighlights square."
        self.rect.setFill('green3')

    def clicked(self,pt):
        """Returns true if pt (click) is inside."""
        if (self.xmin <= pt.getX() <= self.xmax and
                self.ymin <= pt.getY() <= self.ymax):
            self.click = True
            return True
        else:
            return False
