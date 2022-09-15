from threading import Thread
import tkinter
from math import sqrt


active = True

# 1px = 1m
canvas_width = 500
canvas_height = 500

G = 6.67430e5-11

points = []

root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=canvas_height, width=canvas_width, background="black")
# TODO invert the canvas y axis.... No technical improvements but its nicer
canvas.pack()


class Vector:
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction


class Point(Thread):
    def __init__(self, x, y, radius, mass, velocity, force):
        Thread.__init__(self)

        self.x = x
        self.y = y
        self.m = mass
        self.F = force
        self.r = radius
        self.v = velocity

        self.point = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="red")

    def run(self):
        while True:
            for b in points:
                if b != self:
                    # iterates through every point, except for itself
                    f_mag = G * ((self.m * b.m) / dist(self, b) ** 2)


def dist(a, b):
    # TODO check if the passed argument is just a int or a Point object, act accordingly
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def create_point(x, y, radius=5.0, mass=1.0, velocity=0.0, force=Vector(magnitude=0, direction=0)):
    points.append(Point(x, y, radius, mass, velocity, force))


def setup():
    create_point(100, 100)


if __name__ == '__main__':
    setup()

    # make the points alive
    for point in points:
        point.start()
