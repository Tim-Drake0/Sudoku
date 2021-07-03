import pygame
from pygame.locals import *
import time

pygame.init()
pygame.font.init()

black = (0,0,0)
white = (255, 255, 255)
grid = (150, 150, 150)
red = (255, 0, 0)
blue = (0, 109, 255)
highlight = (200, 200, 200)

class Number:
    def __init__(self, left, top, number, pixelSize, isPlayer):
        self.number = number
        self.color = white
        self.isPlayer = isPlayer

        if self.isPlayer:
            self.fontColor = blue
        else:
            self.fontColor = black

        self.rect = Rect(left * pixelSize, top * pixelSize, pixelSize, pixelSize)
        self.pixelSize = pixelSize
        self.getBox()
        self.font = pygame.font.SysFont('couriernew', self.pixelSize)
        self.text = self.font.render(str(self.number), True, self.fontColor)

    def updateNumber(self, newNum):
        self.number = newNum
        self.updateColor()

    def updateColor(self):
        self.text = self.font.render(str(self.number), True, self.fontColor)

    def getBox(self):
        left = self.rect.left // self.pixelSize
        top = self.rect.top // self.pixelSize
        if left <= 2 and top <= 2:
            self.box = 0
        elif left <= 5 and top <= 2:
            self.box = 1
        elif left <= 8 and top <= 2:
            self.box = 2
        elif left <= 2 and top <= 5:
            self.box = 3
        elif left <= 5 and top <= 5:
            self.box = 4
        elif left <= 8 and top <= 5:
            self.box = 5
        elif left <= 2 and top <= 8:
            self.box = 6
        elif left <= 5 and top <= 8:
            self.box = 7
        elif left <= 8 and top <= 8:
            self.box = 8

class Board:
    screenSize = (630, 630)
    pixelSize = screenSize[0] // 9
    mousex = 0
    mousey = 0

    def __init__(self):
        self.width = self.screenSize[0] // self.pixelSize
        self.height = self.screenSize[1] // self.pixelSize
        self.matrix = [[Number(col, row, 0, self.pixelSize, False) for col in range(self.width)] for row in range(self.height)]
        self.screen = pygame.display.set_mode(self.screenSize, RESIZABLE)

    def startGame(self):
        startList = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]

        for rowIndex, row in enumerate(startList):
            for colIndex, num in enumerate(row):
                self.matrix[rowIndex][colIndex].updateNumber(num)
                

        self.topLeftSquareCoords = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 2), (2, 1), (2, 2)]
        self.topLeftSquare = [self.matrix[0][0], self.matrix[0][1], self.matrix[0][2], self.matrix[1][0], self.matrix[1][1], self.matrix[1][2], self.matrix[0][2], self.matrix[2][1], self.matrix[2][2]]

    def drawBoard(self):

        for row in self.matrix:
            for num in row:
                pygame.draw.rect(self.screen, num.color, num.rect)
                if num.number != 0:
                    self.screen.blit(num.text, (num.rect.left + 12, num.rect.top))
                
        # Display the grid lines
        for c in range(0, self.width * self.pixelSize, self.pixelSize):
            for r in range(0, self.height * self.pixelSize, self.pixelSize):
                pygame.draw.rect(self.screen, grid, (c, r, self.pixelSize, self.pixelSize), 1)
        
        pygame.draw.line(self.screen, black, (self.screenSize[0] - (self.screenSize[0] // 3), 0), (self.screenSize[0] - (self.screenSize[0] // 3), self.screenSize[1]), 3)
        pygame.draw.line(self.screen, black, (self.screenSize[0] - ((self.screenSize[0] // 3) * 2), 0), (self.screenSize[0] - ((self.screenSize[0] // 3) * 2), self.screenSize[1]), 3)
        pygame.draw.line(self.screen, black, (0, self.screenSize[1] - (self.screenSize[1] // 3)), (self.screenSize[0], self.screenSize[1] - (self.screenSize[1] // 3)), 3)
        pygame.draw.line(self.screen, black, (0, self.screenSize[1] - ((self.screenSize[1] // 3) * 2)), (self.screenSize[0], self.screenSize[1] - ((self.screenSize[1] // 3) * 2)), 3)

    def checkSameRow(self):
        if self.currentNum.number == 0:
            for row in self.matrix:
                for num in row:
                    if num.fontColor == red:
                        num.fontColor = black
                    num.updateColor()
            return

        for rowIndex, row in enumerate(self.matrix):
            for colIndex, num in enumerate(row):
                if self.currentNum.number == num.number and (rowIndex == self.mousey // self.pixelSize or colIndex == self.mousex // self.pixelSize):
                    num.fontColor = red
                    num.updateColor()

    def checkSameBox(self):
        for row in self.matrix:
            for num in row:
                if self.currentNum.number == num.number and self.currentNum.box == num.box:
                    num.fontColor = red
                    num.updateColor()
                        
    def checkNumbers(self):
        self.checkSameRow() 
        self.checkSameBox()
        self.currentNum.fontColor = blue
        self.currentNum.updateColor()

    def highlightSame(self):
        (self.mousex, self.mousey) = pygame.mouse.get_pos()

        if self.matrix[self.mousey // self.pixelSize][self.mousex // self.pixelSize].number == 0:
            for row in self.matrix:
                for num in row:
                    num.color = white
            self.matrix[self.mousey // self.pixelSize][self.mousex // self.pixelSize].color = highlight
            return

        for rowIndex, row in enumerate(self.matrix):
            for colIndex, num in enumerate(row):
                num.color = white
                if self.matrix[rowIndex][colIndex].number == self.matrix[self.mousey // self.pixelSize][self.mousex // self.pixelSize].number:
                    num.color = highlight

    def checkGame(self):
        for row in self.matrix:
            for num in row:
                if num.number == 0:
                    return False

        return True         

    def gameLoop(self):
        self.startGame()
        while not self.checkGame():
            for event in pygame.event.get():
                if event.type == QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    self.highlightSame()

                if event.type == KEYDOWN:
                    self.currentNum = self.matrix[self.mousey // self.pixelSize][self.mousex // self.pixelSize]
                    if self.currentNum.color == highlight:
                        self.currentNum.number = -1
                        if pygame.key.get_pressed()[pygame.K_KP1] or pygame.key.get_pressed()[pygame.K_1]:
                            self.currentNum.number = 1
                        elif pygame.key.get_pressed()[pygame.K_KP2] or pygame.key.get_pressed()[pygame.K_2]:
                            self.currentNum.number = 2
                        elif pygame.key.get_pressed()[pygame.K_KP3] or pygame.key.get_pressed()[pygame.K_3]:
                            self.currentNum.number = 3
                        elif pygame.key.get_pressed()[pygame.K_KP4] or pygame.key.get_pressed()[pygame.K_4]:
                            self.currentNum.number = 4
                        elif pygame.key.get_pressed()[pygame.K_KP5] or pygame.key.get_pressed()[pygame.K_5]:
                            self.currentNum.number = 5
                        elif pygame.key.get_pressed()[pygame.K_KP6] or pygame.key.get_pressed()[pygame.K_6]:
                            self.currentNum.number = 6
                        elif pygame.key.get_pressed()[pygame.K_KP7] or pygame.key.get_pressed()[pygame.K_7]:
                            self.currentNum.number = 7
                        elif pygame.key.get_pressed()[pygame.K_KP8] or pygame.key.get_pressed()[pygame.K_8]:
                            self.currentNum.number = 8
                        elif pygame.key.get_pressed()[pygame.K_KP9] or pygame.key.get_pressed()[pygame.K_9]:
                            self.currentNum.number = 9
                        elif pygame.key.get_pressed()[pygame.K_BACKSPACE] and self.currentNum.number == 0 or self.currentNum.fontColor != black:
                            self.currentNum.number = 0

                        if self.currentNum.number > -1:
                            self.checkNumbers()

            self.drawBoard() 
            pygame.display.flip()

board = Board()
startTime = time.time()
board.gameLoop()
elapsedTime = time.time() - startTime
print("You win! Time: " + str(elapsedTime) + " seconds.")