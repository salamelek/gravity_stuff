from threading import Thread
import tkinter
from math import sqrt, sin, cos, asin
import Exceptions

active = True

# 1px = 1m
canvas_width = 1000
canvas_height = 1000

G = 6.67430e5 - 11

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

        self.active = True

        self.point = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="red")

    def add_force(self, new_f):
        a = self.F
        b = new_f

        mag_x = a.magnitude * cos(a.direction) + b.magnitude * cos(b.direction)
        mag_y = a.magnitude * sin(a.direction) + b.magnitude * sin(b.direction)

        magnitude = sqrt(mag_x ** 2 + mag_y ** 2)
        direction = asin(mag_y / magnitude)

        self.F = Vector(magnitude=magnitude, direction=direction)

    def run(self):
        while self.active:
            # self.calc_interactions()
            self.calc_actions()

    def move(self, x=0, y=0):
        # TODO 'RuntimeError: main thread is not in main loop' --> https://stackoverflow.com/questions/14694408/runtimeerror-main-thread-is-not-in-main-loop
        # TODO try either updating in the main loop using the new coords or use the mkTkinter lib
        canvas.move(self.point, x, y)

    def calc_interactions(self):
        for point in points:
            if point != self:
                # iterates through every point, except for itself
                f_mag = G * ((self.m * point.m) / dist(self, point) ** 2)
                height = dist((point.x, self.y), point)
                hypotenuse = dist(self, point)
                f_dir = asin(height / hypotenuse)

                self.add_force(Vector(magnitude=f_mag, direction=f_dir))

    def calc_actions(self):
        vx = self.v.magnitude * cos(self.v.direction)
        vy = self.v.magnitude * sin(self.v.direction)
        self.move(vx, vy)

    def stop(self):
        self.active = False


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


def create_point(x, y, radius=5.0, mass=1.0, velocity=Vector(magnitude=0.0, direction=0.0), force=Vector(magnitude=0.0, direction=0.0)):
    points.append(Point(x, y, radius, mass, velocity, force))


def setup():
    create_point(100, 100)


if __name__ == '__main__':
    setup()

    # make the points alive
    for point in points:
        point.start()

    while active:
        try:
            for point in points:
                canvas.move(point, )
            canvas.update()
        except tkinter.TclError:
            active = False
            for point in points:
                point.stop()
            print("Shut down successfully!")
