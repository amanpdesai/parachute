from turtle import *
from time import *               #ALL IMPORTS
from random import *
from threading import *
from time import *
import queue, math

QUEUE_SIZE = 1
s = Screen()
s.setup (width=660, height=510, startx=0, starty=0)
s.bgcolor("#84f9f7")
strike = 0   #Number of parachutes that go into the water. At three Game Over!
points = 0        #How many parachutes the player catches before loosing.

def inscount(x, y, txt, slp):                                             #This function is used for the instructions and countdown in the last few lines
    goto(x, y)
    write(txt, font = ("Arial", 15), align = "center")
    sleep(slp)
    reset()
    penup()
    hideturtle()

def registershapes(image, t):
    s.register_shape(image)
    t.shape(image)
    t.speed(0)
    t.penup()

def f():                       #Boat movement function(forward)
  global boat
  
  boat.backward(10)
  if int(boat.xcor()) >= 330:
    boat.forward(10)

def b():                       #Boat movement function(backward)
  global boat
  boat.forward(10)
  if int(boat.xcor()) <= -330:
    boat.backward(10)

class Boat(Turtle):                                                           #Boat class
  def __init__(self, name):
    Turtle.__init__(self)
    registershapes("/Users/amandesai/Desktop/PICS/costume2.gif", self)        ##If you are planning to run this program the "amandesai" sould be replaced with your computer user and the folder with the pictures should be on your desktop.
    self.right(180)
    self.goto(0, -130)
    self.pencolor("#84f9f7")
    self.penup()
    self.name = name

  def getRadius(self):    #Needed for the intersect function
    return 50

  def move(self):         #Calls f and b for movement of boat
    global s
    s.onkey(f, "Right")
    s.listen()
    s.onkey(b, "Left")
    s.listen()

coords = [[50,300],[-300,-50]]   #Lists inside coords are needed to pick a path for both parachuts


class Parachute(Turtle):                           #Parachute class
  def __init__(self, boat, name, x, y, img):
    super().__init__()
    self.speed(0)
    self.penup()
    self.left(90)
    self.hideturtle()
    self.goto(x, y)
    self.shape(img)         #sets shape
    tmp = randint(0,1)      #takes random num one or zero
    x1 = coords[tmp]        #takes a list from coords
    #print("x1:" + str(x1))
    self.rx = randint(coords[tmp][0],coords[tmp][1]) #The selected list is used to put in parameters for a section for the parachute movement.
    self.Boat = boat                                  #needed for the intersect check
    self.name = name                                     #needed for threading
    
  def resetPara(self):                                    #function is used for reseting parachute to the copter's position
    self.speed(0)
    self.hideturtle()
    self.goto(265, 200)              #takes random num one or zero
    tmp = randint(0,1)             #takes a list from coords
    self.rx = randint(coords[tmp][0],coords[tmp][1])     #The selected list is used to put in new parameters for a section for the parachute movement.

  def getRadius(self):   #needed for the intersect function
    return 50

  def move(self):              #function that moves parachutes
    global points, strike
    self.showturtle()
    self.penup()
    y = -130                 #Used for making a set y-coordinate ending point
    tracer(False)           #Used to speed up parachutes only
    self.speed(0.0001)       #Used for decreasing speed a little or else the result is instant
    mx = int(self.xcor())    #Gives mx the integer version of x coordinate of parachute         slope is from here--->|
    my = int(self.ycor())    #Gives my the integer version of y coordinate of parachut                                |
    nx = mx - self.rx        #Needed to find the length of the slope                                                  |
    ny = my - y              #Needed to find hight of slope                         to here  ----->___________________|      
    #print("nx:" + str(nx) + " ny:" + str(ny) + "mx:" + str(mx) + " my:" + str(my) + " rx:" + str(self.rx))
    if nx == 0:         #checks if nx is zero so that program is not dividing by zero
        nx = nx + 1     #If yes then nx + 1 if no then continue
    self.goto((mx - 1), (my - (ny/nx)))       #this line is basically moving the parachute left one pixel and down by the hight of the slope by the length of the slope
    if int(self.ycor()) >= 255:
        self.resetPara()
    tracer(True)             #Turns off tracer
    if intersect(self.Boat, self):     #Calls the intersect function to check if parachute touches boat
        self.resetPara()           #Calls the reset function to reset the parachute
        color("#84f9f7")           #Changes the color of the turtle
        goto(-265, 200)              #goes to the top right corner
        write("POINTS : " + str(points), font = ("Arial", 15), align = "center")        #Overwrites the points in the background color
        points = points + 1              #Adds one to points
        color("black")                   #Changes the turtle color to black
        write("POINTS : " + str(points), font = ("Arial", 15), align = "center")        #writes the new score
    elif int(self.ycor()) <= int(self.Boat.ycor()):            #Checks if parachutes y coordinate is less or equal to boat
        self.resetPara()            #Resets parachute
        color("#84f9f7")            #Changes the color of the turtle
        goto(-265, 170)               #goes to the top right corner
        write("STRIKES : " + str(strike), font = ("Arial", 15), align = "center") #Overwrites the strikes in the background color
        strike = strike + 1         #adds one to strike
        color("black")               #Changes the turtle color to black
        write("STRIKES : " + str(strike), font = ("Arial", 15), align = "center")        #writes the new score

def intersect(object1,object2):            #Intersect function was taken from https://trinket.io/python/e3f2e3e371
  dist = math.sqrt((object1.xcor() - object2.xcor())**2 + (object1.ycor() - object2.ycor())**2)
  radius1 = object1.getRadius()
  radius2 = object2.getRadius()

  if dist <= radius1+radius2:
      return True
  else:
      return False

class MyTurtleManipulator(Thread):          #This class is assigned to a thread. Most of the threading was new to me so I took the threading functions from https://stackoverflow.com/questions/5846854/tkinter-turtles-and-threads

    def __init__(self, turtle):
        super().__init__()           #This line is essentially a short cut that calls the init function
        self.turtle = turtle         #assigns the word given into the parameters to turtle 

    def run(self):                #This function is used to enter the move from each turtle that is given into the queue of what to do
        while not(strike >= 3):                                    #Repeats untill strike is three
            actions.put((self.turtle, self.turtle.move))           #Enters a turtle and a function from the turtles class that is entered into a queue of things to run

def process_queue():                                #This function is used to process the queue
    global strike
    while not actions.empty():                      #This loop runs untill there are no more items in the list to perform
        turtle, action = actions.get()              #This line basically removes a turtle and an action from the list
        action()                     #This line runs the function and turtle that were removed from the list               
        if (strike >=3):             #If strikes are at three or greater, next line breaks the loop
            break

    if (active_count() > 1 and strike < 3):     #Checks if number of items in the list is greater than one and strikes are less than three
        s.ontimer(process_queue, 1)             #Starts a  screen timer and once the timer is done(one millisecond), it starts to process the queue
    else:                                       #else
        goto(-30, 0)                              #sends the turtle to a point
        color("red")                 #color red
        write("GAME OVER!", font = ("Arial", 50), align = "center")                  #writes game over 
 
actions = queue.Queue(QUEUE_SIZE)          #sets actions to a queue and sets the queue size to the value of QUEUE_SIZE 

s.register_shape("/Users/amandesai/Desktop/PICS/Mr_Game___Watch_SSB4.gif")       #adds shape(Need to specify location otherwize it will give error
boat = Boat("Boat")                  #sets boat to class Boat
para1 = Parachute(boat, "para1", 265, 200, "/Users/amandesai/Desktop/PICS/Mr_Game___Watch_SSB4.gif")        #assigns para1 to Parachute class (gives boat for intersect function, gives start coordinats, and gives shape
para2 = Parachute(boat, "para2", 265, 200, "/Users/amandesai/Desktop/PICS/Mr_Game___Watch_SSB4.gif")        #assigns para2 to Parachute class (gives boat for intersect function, gives start coordinats, and gives shape

def setUp():                                                              #Sets up all other items in the screen
    global s
    global points
    tree = Turtle()                                                                   #this line to the goto is all tree setup
    registershapes("/Users/amandesai/Desktop/PICS/costume.gif", tree)                #Calls function registershapes
    tree.left(90)                                                                     #Turns tree so it is not sideways
    tree.goto(265, -45)                                                               #moves the tree to its position
    speed(0)                                                                          #From this line to end_fill turtle is drawing water
    penup()
    goto(0, -150)
    hideturtle()
    color("#1fc4c8")
    pendown()
    begin_fill()
    forward(340)
    right(90)
    forward(260)
    right(90)
    forward(680)
    right(90)
    forward(260)
    right(90)
    forward(340)
    end_fill()
    copter = Turtle()                                                             #from this line to copter.goto, all lines are for copter setup
    registershapes("/Users/amandesai/Desktop/PICS/costume1.gif", copter)
    copter.penup()
    copter.left(90)
    copter.goto(265, 200)
    penup()                                                                     #From this line to end of function, turtle is writing score and strike
    color("black")
    goto(-265, 200)
    
    pendown()
    write("POINTS : " + str(points), font = ("Arial", 15), align = "center")
    penup()
    goto(-265, 170)
    pendown()
    write("STRIKES : " + str(strike), font = ("Arial", 15), align = "center")
    penup()
    hideturtle()
    
penup()                           #From this line to last hideturtle, turtle is writing instructions and shows an on screen timer of three seconds
hideturtle()
color("black")
inscount(-45, -7.5, "Welcome to Parachute Catcher!", 5)
inscount(-45, -7.5, "Use the Left and Right arrow keys to move.", 5)
inscount(-30, -7.5, "In this game your goal is to catch as many parachutes as you can.", 8)
inscount(-30, -7.5, "However do not let them hit the water.", 5)
inscount(-30, -7.5, "You have three strikes before you lose.", 5)
inscount(-20, -7.5, "Good Luck!", 3)
inscount(-5, -10, "3", 1)
inscount(-5, -10, "2", 1)
inscount(-5, -10, "1", 1)
inscount(-5, -10, "GOOO!", 3)

setUp()                                     #Calls setup
MyTurtleManipulator(para1).start()         #Calls MyTurtleManipulator and gives it the para1 turtle and starts the threading
MyTurtleManipulator(para2).start()         #Calls MyTurtleManipulator and gives it the para2 turtle and starts the threading
MyTurtleManipulator(boat).start()          #Calls MyTurtleManipulator and gives it the boat turtle and starts the threading

process_queue()    #Tells process queue to start all functions in its list

s.mainloop()       #Starts the main code for the turtle program(always has to be the last line in a turtle program.)
