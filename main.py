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

P0 = 100000.0
RoomTemprature = 293.0
UnitLength = 2.0

gravity_force = [0 , -9.8]

balls = []
platforms = []

class ball():

    def init_turtle(self):
        self.turtle_obj = turtle.Turtle()
        self.turtle_obj.penup()
        self.turtle_obj.hideturtle()
        self.turtle_obj.shape('circle')
        self.turtle_obj.turtlesize(self.radius * UnitLength, self.radius * UnitLength, 0)
        self.turtle_obj.speed(0)
        self.turtle_obj.showturtle()
 
    def __init__(self, mass: float, radius: float, position: list[float] = [0, 0], temprature:float = RoomTemprature, pressure:float = P0, coefficient_of_restitution:float = 0.5):
        self.mass = mass
        self.radius = radius
        self.volume = (4/3) * math.pi * (radius**3)
        self.density = self.mass / self.volume
        self.temprature = temprature
        self.pressure = pressure
        self.position = position
        self.acceleration = [0 , 0]
        self.force = [0 , 0]
        self.speed = [0 , 0]
        self.horizontal_x_range = [self.position[0] - (radius/2), self.position[0] + (radius/2)]
        self.vertical_y_range = [self.position[1] - (radius/2), self.position[1] + (radius/2)]
        self.coefficient_of_restitution = coefficient_of_restitution
        self.dt = 0
        self.kinetik_energy = 0;
        self.thermal_energy = 0;
        self.potential_energy = position[1] * mass * gravity_force[1];
        self.internal_energy = self.kinetik_energy + self.thermal_energy + self.potential_energy;
        self.init_turtle()
        self.update()
        balls.append(self)

    def display(self):
        self.turtle_obj.goto(self.position)

    def setDt(self, dt):
        self.dt = dt

    def update(self):
        self.accelerate()
        self.move()
        self.display()

    def move(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        self.horizontal_x_range = [self.position[0] - (self.radius/2), self.position[0] + (self.radius/2)]
        self.vertical_y_range = [self.position[1] - (self.radius/2), self.position[1] + (self.radius/2)]

    def accelerate(self):
        self.speed[0] += self.acceleration[0]
        self.speed[1] += self.acceleration[1]
        self.acceleration = [0, 0]

    def applyForce(self, force: list[float]):
        self.force[0] += force[0]
        self.force[1] += force[1]
        self.acceleration[0] += self.force[0] * UnitLength * self.mass
        self.acceleration[1] += self.force[1] * UnitLength * self.mass
        self.force[0] -= force[0]
        self.force[1] -= force[1]

    def calculateBounceUp(self, force: list[float]):
        bounce_force = [force[0], (- self.speed[1]) + (- (self.speed[1] * self.coefficient_of_restitution)) ] 
        return bounce_force


class platform():
    def __init__(self, position: list[float], length = 5, width = 1):
        self.position = position
        self.length = length
        self.width = width
        self.horizontal_x_range = [self.position[0] - (length/2), self.position[0] + (length/2)]
        self.vertical_y_range = [self.position[1] - (width/2), self.position[1] + (width/2)]
        self.init_turtle()
        self.update()
        platforms.append(self)

    def init_turtle(self):
        self.turtle_obj = turtle.Turtle()
        self.turtle_obj.penup()
        self.turtle_obj.hideturtle()
        self.turtle_obj.shape('square')
        self.turtle_obj.turtlesize(self.length * UnitLength, self.width * UnitLength, 0)
        self.turtle_obj.speed(0)
        self.turtle_obj.showturtle()

    def display(self):
        self.turtle_obj.goto(self.position)

    def setDt(self, dt):
        self.dt = dt

    def move(self, newPosition: list[float]):
        self.position = newPosition

    def update(self):
        self.display()


def checkCollission():
    for unique_ball_obj in balls:
        for unique_platform_obj in platforms:
            if (unique_ball_obj.vertical_y_range[0] < unique_platform_obj.vertical_y_range[1]):
                unique_ball_obj.applyForce(unique_ball_obj.calculateBounceUp(unique_ball_obj.force))


B = ball(mass = 0.5, radius = 1, position = [0 , 200], coefficient_of_restitution = 0.88)
Ground = platform(position = [0, -200], length = 1, width = 5)

while 1:
    delta_t = 0.01
    B.setDt(delta_t)

    current_force = [gravity_force[0] * delta_t, gravity_force[1] * delta_t]
    B.applyForce(current_force)
    checkCollission()
    
    B.update()

turtle.Screen().exitonclick()
