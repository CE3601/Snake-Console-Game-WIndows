class SnakePart():
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

class Snake():

    #direction mapped to a multiplyer
    directions_x = {"RIGHT" : 1, "LEFT" : -1, "NULL" : 0}
    directions_y = { "UP" : -1, "DOWN" : 1, "NULL" : 0}

    def __init__(self, initial_x, initial_y, symbol, speed, direction):
        #Every snake begins with an initial snakePart object
        #Snake body will be a list of snakePart objects
        #The tail is a list of values that account for the last snake object
        self.snake_head = SnakePart(initial_x, initial_y, symbol)
        self.snake_body = []
        self.tail = [initial_x, initial_y, direction]
        self.speed = speed

    def changePosition(self,dir_x, dir_y):
        #Previous position data is stored
        prev_x, prev_y = self.snake_head.x, self.snake_head.y

        #move the snakes head
        self.snake_head.x = prev_x + Snake.directions_x[dir_x]
        self.snake_head.y = prev_y + Snake.directions_y[dir_y]

        if self.snake_body:
            #containers for the next x, y coordinates
            next_x, next_y = 0, 0
            for body_part in self.snake_body:
                #change the coordinates of each body part
                next_x, next_y = body_part.x, body_part.y
                body_part.x, body_part.y = prev_x, prev_y
                prev_x, prev_y = next_x, next_y

        self.updateTail(dir_x) if dir_x != "NULL" else self.updateTail(dir_y)

    def updateTail(self, dir):
        #Because the tail is used to append a snake part, it should be updated on each movement
        if self.snake_body:
            self.tail[0] = self.snake_body[-1].x
            self.tail[1] = self.snake_body[-1].y
        else:
            self.tail[0] = self.snake_head.x
            self.tail[1] = self.snake_head.y
        self.tail[2] = dir

    def addPart(self):
        x, y = self.tail[0], self.tail[1]
        tail_dir = self.tail[2]

        if tail_dir == "UP":
            self.snake_body.append(SnakePart(x, y+1, self.snake_head.symbol))

        elif tail_dir == "DOWN":
            self.snake_body.append(SnakePart(x, y-1, self.snake_head.symbol))

        elif tail_dir == "RIGHT":
            self.snake_body.append(SnakePart(x-1, y, self.snake_head.symbol))

        else:
            self.snake_body.append(SnakePart(x+1, y, self.snake_head.symbol))

class Fruit():

    def __init__(self, symbol, value, x, y):
        self.symbol = symbol
        self.value = value
        self.x = x
        self.y = y
