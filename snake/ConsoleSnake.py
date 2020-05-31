"""
    Run a game of snake through console
"""

from snake  import *
import random
import curses
import os

class ConsoleSnake():

    directions = {curses.KEY_UP,curses.KEY_DOWN,curses.KEY_LEFT,curses.KEY_RIGHT}

    def __init__(self, snake_symbol, speed, initial_x, initial_y):
        """Initializes snake object and the curses terminal window"""
        self.snake = Snake(initial_x, initial_y, snake_symbol, speed, "RIGHT")
        self.fruits = []
        self.current_direction = curses.KEY_RIGHT
        self.score = "0"

        #use system function to set the console size
        os.system("mode con cols=50 lines=40")

        #Initialize screen, create a box border,
        #Set nodelay to handle inputs
        self.game_win = curses.initscr()
        self.game_win.box()
        self.game_win.nodelay(True)
        self.game_win.keypad(True)
        self.game_win.refresh()

        #SetUp the curses module
        curses.noecho()
        curses.curs_set(False)

        #The console width and height data saved
        self.win_height, self.win_width = self.game_win.getmaxyx()

    def endGameWindow(self):
        #Re-establishes terminal settings and ends the window
        curses.echo()
        curses.endwin()

    def clearScreen(self):
        #Clear and rebox the screen
        self.game_win.clear()
        self.game_win.box()

    def moveSnake(self, direction):
        #Changes coordinates of the snake head
        current_x, current_y = self.snake.snake_head.x, self.snake.snake_head.y

        if direction == curses.KEY_LEFT:
            self.snake.changePosition("LEFT", "NULL")

        elif direction == curses.KEY_RIGHT:
            self.snake.changePosition("RIGHT", "NULL")

        elif direction == curses.KEY_DOWN:
            self.snake.changePosition("NULL", "DOWN")

        else:
            self.snake.changePosition("NULL","UP")

    def detectWallCollision(self):
        #Check the snake input against the console demensions
        if self.snake.snake_head.x == self.win_width - 1 or self.snake.snake_head.y == self.win_height - 1:
            return True
        elif self.snake.snake_head.x == 0 or self.snake.snake_head.y == 0:
            return True

    def detectFruitCollison(self):
        #Loop through the fruits
        for fruit in self.fruits:
            if self.snake.snake_head.x == fruit.x and self.snake.snake_head.y == fruit.y:
                #setting the fruit coordinates to (None,None)
                self.fruits.remove(fruit)
                return True

    def detectBodyCollision(self):
        if self.snake.snake_body:
            for body_part in self.snake.snake_body:
                if self.snake.snake_head.x == body_part.x and self.snake.snake_head.y == body_part.y:
                    return True

    def drawSnake(self):
        #draw the snakes head
        current_x, current_y = self.snake.snake_head.x, self.snake.snake_head.y
        self.game_win.addch(current_y, current_x, self.snake.snake_head.symbol)
        #draw the body
        if self.snake.snake_body:
            for body_part in self.snake.snake_body:
                self.game_win.addch(body_part.y, body_part.x, body_part.symbol)

    def drawScore(self):
        #Outpts the score in the upper right of the window
        self.game_win.addstr(1, self.win_width - 10,"SCORE: " + self.score)

    def addFruits(self, n):
        #Function to randomly place N fruits on the screen
        for i in range(n):
            self.fruits.append(
            Fruit("F", 1, random.randint(1, self.win_width-2), random.randint(1, self.win_height-2)))

    def drawFruit(self):
        if self.fruits:
            for fruit in self.fruits:
                self.game_win.addch(fruit.y, fruit.x, fruit.symbol)

    def main(self):

        #SetUP:
        ESC = 27
        running = True
        running_score = 0
        self.addFruits(1)

        #GameLoop
        while running:
            #DRAW componants:
            self.drawSnake()
            self.drawFruit()
            self.drawScore()
            self.game_win.refresh()

            #LOGIC
            self.moveSnake(self.current_direction)
            key = self.game_win.getch()
            if key in self.directions:
                self.current_direction = key
            elif key == ESC or self.detectWallCollision() or self.detectBodyCollision():
                #End the curses application
                running = False
                message = "Escape Key Pressed\n" if key == ESC else "Collision detected\n"
                print(message)
                self.endGameWindow()

            #IF all fruits have been eaten, add fruits.
            if not self.fruits:
                self.addFruits(running_score)

            if self.detectFruitCollison():
                self.snake.addPart()
                running_score += 1
                self.score = str(running_score)

            #Control
            curses.napms(50)
            self.clearScreen()

if __name__ == "__main__":

    run = ConsoleSnake("0", 1, 20, 5)
    run.main()
