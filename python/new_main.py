import tkinter

from math import sqrt, sin, asin, pi, cos
import time

import Exceptions


active = True

# 1px = 1m
canvas_width = 1000
canvas_height = 1000

G = 6.67430e5#-11

points = []

root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=canvas_height, width=canvas_width, background="black")
# TODO invert the canvas y axis.... No technical improvements but its nicer
canvas.pack()


class Vector:
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction


class Point:
    def __init__(self, x, y, radius, velocity, mass, force, a, time):
        self.x = x
        self.y = y
        self.a = a
        self.m = mass
        self.F = force
        self.r = radius
        self.v = velocity
        self.t = time

        self.point = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="red")

    def add_force(self, force):
        a = self.F
        b = force

        # fx = ax + bx ...
        fx = a.magnitude * cos(a.direction) + b.magnitude * cos(b.direction)
        fy = a.magnitude * sin(a.direction) + b.magnitude * sin(b.direction)
        magnitude = sqrt(fx ** 2 + fy ** 2)
        direction = asin(fy / magnitude)
        # print(magnitude, direction)
        # print(direction)

        self.F.magnitude = magnitude
        self.F.direction = direction

    def move(self, x=0.0, y=0.0):
        # update all the values
        self.x += x
        self.y += y

        self.a = self.F.magnitude / self.m
        # TODO should be +=, but its all directional :')
        self.v = self.a * (time.time() - self.t)

        canvas.move(self.point, x, y)

    def update_time(self):
        self.t = time.time()


def dist(a, b):
    if type(a) == tuple:
        ax = a[0]
        ay = a[1]

    elif type(a) == Point:
        ax = a.x
        ay = a.y

    else:
        raise Exceptions.IncorrectoPointCoordsError(a)

    if type(b) == tuple:
        bx = b[0]
        by = b[1]

    elif type(b) == Point:
        bx = b.x
        by = b.y

    else:
        raise Exceptions.IncorrectoPointCoordsError(b)

    return sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def check_pos():
    # check that no points are beyond the border
    # check that no points are stuck in each other
    pass


def calc_interactions():
    if len(points) > 1:
        for i in range(len(points)):
            for j in range(len(points) - (i + 1)):
                a = points[i]
                b = points[j + 1 + i]

                # iterates through every interaction
                # for every iteration it sums the current F with the previous F (of every new frame F is 0)

                # magnitude of Fa and Fb
                magnitude = G * ((a.m * b.m) / dist(a, b) ** 2)

                # direction of Fa and Fb
                direction_a = asin(abs(b.y - a.y) / dist(a, b))
                direction_b = direction_a + pi

                # add Fa and Fb
                fa = Vector(
                    magnitude=magnitude,
                    direction=direction_a
                )
                fb = Vector(
                    magnitude=magnitude,
                    direction=direction_b
                )

                a.add_vectors(fa)

                # only on last
                # if i == len(points) - 1:
                #     b.add_force(fb)


def calc_actions():
    for point in points:
        # calculate vx, vy from vector
        # set x and y in relation to TIME PASSED, not frame
        fi = point.F.direction
        v = point.v
        t = time.time() - point.t
        point.move(cos(fi) * v * t, sin(fi) * v * t)

        # TODO if im not wrong, using a will mean no resetting
        # reset F
        # point.F.magnitude = 0
        # point.F.direction = 0


def update_time():
    for point in points:
        point.update_time()


def create_point(x, y, radius=5, velocity=0.0, mass=1.0, a=0.0, force=Vector(magnitude=0.0, direction=0.0), time=time.time()):
    points.append(Point(x=x, y=y, radius=radius, velocity=velocity, mass=mass, force=force, a=a, time=time))


def setup():
    # create_point(400, 500)
    create_point(600, 500, velocity=5, force=Vector(0, pi/2))


if __name__ == '__main__':
    setup()

    while active:
        check_pos()

        try:
            canvas.update()
        except tkinter.TclError:
            active = False
            print("Shut down successfully!")

        calc_interactions()
        calc_actions()
        update_time()
