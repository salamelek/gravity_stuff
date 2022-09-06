import tkinter
import random
import time
from math import sqrt


active = True

canvas_width = 1000
canvas_height = 1000

G = 6.67430e-11

points = []

root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=canvas_height, width=canvas_width, background="black")
canvas.pack()


class Force:
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction


class Point:
    def __init__(self, x, y, radius, velocity, mass, force):
        self.x = x
        self.y = y
        self.m = mass
        self.F = force
        self.r = radius
        self.v = velocity

        self.point = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="red")

    def add_force(self, force):
        pass


def create_point(x, y, radius=5, velocity=0.0, mass=1.0, force=Force(magnitude=0.0, direction=0.0)):
    points.append(Point(x=x, y=y, radius=radius, velocity=velocity, mass=mass, force=force))


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


def calc_actions():
    pass


def setup():
    create_point(350, 350)
    create_point(650, 425)
    create_point(500, 450)


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
