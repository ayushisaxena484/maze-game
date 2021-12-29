import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Game By Patrick Burns")
wn.setup(700,700)
wn.tracer(0)

#Register Shapes
turtle.register_shape("wizzl-1.gif")
turtle.register_shape("wizzr-2.gif")
turtle.register_shape("loot-1.gif")
turtle.register_shape("wall-1.gif")
turtle.register_shape("enemy.gif")

#Create Class
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wizzr-2.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 0 

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
 
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
 
    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
 
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
 
    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()

        self.shape("wizzl-1.gif")
 
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
 
    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        self.shape("wizzr-2.gif")
 
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2) )            

            
        if distance < 5:
            return True
        else:
            return False


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("loot-1.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100    
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)    
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("enemy.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
            self.shape("enemy.gif")
        elif self.direction == "right":
            dx = 24
            dy = 0
            self.shape("enemy.gif")
        else:
            dx = 0
            dy = 0

        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        #Calculate the spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        #Check to see if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            #Choose a different direction
            self.direction = random.choice(["up", "down", "left", "right"])

        #Set a timer to move next time
        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        a = self.xcor()-other.xcor()
        b=self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) +(b ** 2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle();
        
#Create levels list
levels = [""]

#Define First Level
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXE        XXXXX",
"X  XXXXXXX  XXXXXX  XXXXX",
"X       XX  XXXXXX  XXXXX",
"X       XX  XXX        XX",
"XXXXXX  XX  XXXE       XX",
"XXXXXX  XX  XXXXXX  XXXXX",
"XXXXXX  XX    XXXX  XXXXX",
"X  XXX        XXXX TXXXXX",
"X  XXX  XXXXXXXXXXXXXXXXX",
"X         XXXXXXXXXXXXXXX",
"XE               XXXXXXXX",
"XXXXXXXXXXXX     XXXXXT X",
"XXXXXXXXXXXXXXX  XXXXX  X",
"XXXT XXXXXXXXXX         X",
"XXXE                    X",
"XXX         XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX              X",
"XXT  XXXXXE             X",
"XX   XXXXXXXXXXXXX  XXXXX",
"XX    YXXXXXXXXXXX  XXXXX",
"XX          XXXX       TX",
"XXXXE                   X",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]

#Add a treasure list
treasures = []

#Add enemies list
enemies = []

#Add maze to mazes list
levels.append(level_1)

#Create Level Setup Function
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            #Get the character at each x,y coordinate
            #NOTE the order of y and x in the next line
            character = level[y][x]
            #Calculate the screen x, y coordinates
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

#Check if it is an X (representing a wall)
            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall-1.gif")
                pen.stamp()
                #Add coordinates to wall list
                walls.append((screen_x, screen_y))

#Check if it is a P (representing the player)
            if character == "P":
                player.goto(screen_x, screen_y)

#Check if it is a T (representing the treasure)
            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))

#Check if it is a E (representing the enemy)
            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))

#Create class instances
pen = Pen()
player = Player()

#Create wall coordinate list
walls = []

#Set up the level
setup_maze(levels[1])

#KeyBoard Binding
turtle.listen()
turtle.onkeypress(player.go_left,"Left")
turtle.onkeypress(player.go_right,"Right")
turtle.onkeypress(player.go_up,"Up")
turtle.onkeypress(player.go_down,"Down")

#Turn off screen updates
wn.tracer(0)

#Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

#Main Game Loop
while True:
     #Checks for player collision with treaure
    #Iterate through treaure list
    for treasure in treasures:
        if player.is_collision(treasure):
            #Add the treasure gold to the player gold
            player.gold += treasure.gold
            print ("Player Gold: {}".format(player.gold))
            #Destroy the treasure
            treasure.destroy()
            #Remove the treasure from the treasures list
            treasures.remove(treasure)

    #Iterate through enemy list to see if the player collided
            for enemy in enemies:
                if player.is_collision(enemy):
                    print ("Player dies!")
 
            
    wn.update()

