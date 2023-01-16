import pygame
from math import pi, sin, asin, sqrt, cos
import time

import Exceptions

pygame.init()

active = True
target_fps = 360
width = 1200
height = 650
bcg_color = "black"
objects = []
G = 6.67430e5  # -11

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()


class Vector:
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction

    def print_self(self):
        print("=======================")
        print(f"Force: {self.magnitude} N\nDirection: {self.direction * (180 / pi)} DEG | {self.direction} RAD")
        print("=======================")


class Ball:
    def __init__(self, x, y, radius, velocity, mass, force, acceleration, time):
        self.x = x
        self.y = y
        self.m = mass
        self.F = force
        self.r = radius
        self.v = velocity
        self.a = acceleration
        self.time = time

    def update(self):
        pygame.draw.circle(screen, "red", (self.x, self.y), self.r, 0)
        self.time = time.time()


def add_vectors(vect_a, vect_b):
    a = vect_a
    b = vect_b

    fx = a.magnitude * cos(a.direction) + b.magnitude * cos(b.direction)
    fy = a.magnitude * sin(a.direction) + b.magnitude * sin(b.direction)
    magnitude = sqrt((fx ** 2) + (fy ** 2))

    if magnitude != 0.0:
        direction = asin(fy / magnitude)

        # there are 4 quadrants
        if fx < 0:
            direction = pi - direction

    else:
        # since there is no force, the direction is useless
        direction = 0.0

    return Vector(magnitude=magnitude, direction=direction)


def dist(a, b):
    if type(a) == tuple:
        ax = a[0]
        ay = a[1]

    elif type(a) == Ball:
        ax = a.x
        ay = a.y

    else:
        raise Exceptions.IncorrectoPointCoordsError(a)

    if type(b) == tuple:
        bx = b[0]
        by = b[1]

    elif type(b) == Ball:
        bx = b.x
        by = b.y

    else:
        raise Exceptions.IncorrectoPointCoordsError(b)

    return sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def create_point(x, y, radius=5, velocity=Vector(magnitude=0, direction=0), mass=1.0, acceleration=Vector(magnitude=0, direction=0), force=Vector(magnitude=0.0, direction=0.0), my_time=time.time()):
    objects.append(Ball(x=x, y=y, radius=radius, velocity=velocity, mass=mass, force=force, acceleration=acceleration, time=my_time))


def render():
    screen.fill(bcg_color)

    for my_object in objects:
        my_object.update()

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # Limit to 60 frames per second
    clock.tick(target_fps)


def calc_interactions():
    if len(objects) > 1:
        # iterates through every interaction
        for i in range(len(objects)):
            for j in range(len(objects) - (i + 1)):
                a = objects[i]
                b = objects[i + j + 1]


def calc_actions():
    for my_object in objects:
        # convert forces to accelerations
        acceleration_magnitude = my_object.F.magnitude
        acceleration_direction = my_object.F.direction
        new_acceleration = Vector(magnitude=acceleration_magnitude, direction=acceleration_direction)

        # add new acceleration
        my_object.a = add_vectors(my_object.a, new_acceleration)

        # convert accelerations to velocities
        velocity_magnitude = my_object.a.magnitude * (time.time() - my_object.time)
        velocity_direction = my_object.a.direction
        new_velocity = Vector(magnitude=velocity_magnitude, direction=velocity_direction)

        # add new velocity
        my_object.v = add_vectors(my_object.v, new_velocity)

        # move
        my_object.x += my_object.v.magnitude * cos(my_object.v.direction) * (time.time() - my_object.time)
        my_object.y += my_object.v.magnitude * sin(my_object.v.direction) * (time.time() - my_object.time)

        # check for walls collision
        if my_object.x > width - my_object.r or my_object.x < my_object.r:
            # change the direction of the object
            my_object.v.direction = 0
            # teleport the object back where the collision should be
        if my_object.y > height - my_object.r or my_object.y < my_object.r:
            # change the direction of the object
            my_object.v.direction = -(pi/2)
            # teleport the object back where the collision


def update():
    for my_object in objects:
        my_object.update()


def setup():
    create_point(50, 50, velocity=Vector(0, 0), acceleration=Vector(9.81, pi/2))


if __name__ == '__main__':
    setup()
    while active:
        render()
        calc_interactions()
        calc_actions()
        update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
