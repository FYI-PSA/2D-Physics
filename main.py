import turtle
import time
import math

# MASS UNITS   :   KILO GRAMS
# LENGTH UNITS :   METERS
# TEMP UNITS :     KELVINS
# TIME UNITS :     SECONDS

# ENERGY :         JULES
# PRESSURE UNITS : PASCALS
# DENSITY :        KILO GRAMS / METERS

# cordinates are measured by length units

# call every X turtle pixels 1 length unit

P0 = 100000
RoomTemprature = 293
UnitLength = 2

class ball():

    def init_turtle(self):
        self.turtle_obj = turtle.Turtle()
        self.turtle_obj.penup()
        self.turtle_obj.hideturtle()
        self.turtle_obj.shape('circle')
        self.turtle_obj.turtlesize(self.radius * UnitLength, self.radius * UnitLength, 0)
        self.turtle_obj.speed(0)
        self.turtle_obj.showturtle()
 
    def __init__(self, mass: int, radius: int, position: list[int] = [0, 0], temprature:int = RoomTemprature, pressure:int = P0, coefficient_of_restitution = 0.5):
        self.mass = mass
        self.radius = radius
        self.volume = (4/3) * math.pi * (radius**3)
        self.density = self.mass / self.volume
        self.temprature = temprature
        self.pressure = pressure
        self.position = position
        self.acceleration = [0 , 0]
        self.internal_energy = 0;
        self.force = [0 , 0]
        self.speed = [0 , 0]
        self.coefficient_of_restitution = coefficient_of_restitution
        self.dt = 0
        self.init_turtle()

    def display(self):
        self.turtle_obj.goto(self.position)

    def setDt(self, dt):
        self.dt = dt

    def update(self):
        self.accelerate()
        self.move()

    def move(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]

    def accelerate(self):
        self.speed[0] += self.acceleration[0]
        self.speed[1] += self.acceleration[1]
        self.acceleration = [0, 0]

    def applyForce(self, force: list[int]):
        self.force[0] += force[0]
        self.force[1] += force[1]
        self.acceleration[0] += self.force[0] * UnitLength * self.mass
        self.acceleration[1] += self.force[1] * UnitLength * self.mass
        self.force[0] -= force[0]
        self.force[1] -= force[1]

    def calculateBounceUp(self, force: list[int]):
        bounce_force = [force[0], (- self.speed[1]) + (- (self.speed[1] * self.coefficient_of_restitution)) ] 
        return bounce_force

B = ball(mass = 0.5, radius = 1, position = [0 , 200], coefficient_of_restitution = 0.88)

gravity_force = [0 , -9.8]

old_t = time.time()
while 1:
    new_t = time.time()
    delta_t = new_t - old_t
    if (delta_t < 0.00000001):
        delta_t = 0.00000001
    B.setDt(delta_t)
    old_t = new_t 

    current_force = [gravity_force[0] * delta_t, gravity_force[1] * delta_t]

    if (B.position[1] < -100):
        current_force = B.calculateBounceUp(current_force)
    
    B.applyForce(current_force)
    B.update()
    B.display()

turtle.Screen().exitonclick()
