from threading import Thread
import tkinter
from math import sqrt, sin, cos, asin
import Exceptions
import time

active = True

# 1px = 1m
canvas_width = 500
canvas_height = 500

G = 6.67430e-11

points = []

root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=canvas_height, width=canvas_width, background="black")
# TODO invert the canvas y axis.... No technical improvements but its nicer
canvas.pack()


class Vector:
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction


def add_forces(vect_a, vect_b):
    a = vect_a
    b = vect_b

    mag_x = a.magnitude * cos(a.direction) + b.magnitude * cos(b.direction)
    mag_y = a.magnitude * sin(a.direction) + b.magnitude * sin(b.direction)

    magnitude = sqrt(mag_x ** 2 + mag_y ** 2)
    if magnitude == 0.0:
        direction = 0
    else:
        direction = asin(mag_y / magnitude)

    return Vector(magnitude=magnitude, direction=direction)


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

    return sqrt((bx - ax) ** 2 + (by - ay) ** 2)


class Point(Thread):
    def __init__(self, x, y, radius, mass, velocity, force, acceleration):
        Thread.__init__(self)

        # constant forces
        self.const_F = force
        self.const_v = velocity
        self.const_a = acceleration

        self.x = x
        self.y = y
        self.m = mass
        self.r = radius
        self.time = time.time()
        self.F = self.const_F
        self.v = self.const_v
        self.a = self.const_a

        self.active = True

        self.point = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="red")

    def run(self):
        while self.active:
            for b in points:
                if b != self:
                    # add up all the forces
                    f_mag = G * ((self.m * b.m) / (dist(self, b) ** 2))
                    height = dist((b.x, self.y), b)
                    hypotenuse = dist(self, b)
                    f_dir = asin(height / hypotenuse)

                    self.F = add_forces(self.F, Vector(magnitude=f_mag, direction=f_dir))

            # convert calculated force to acceleration
            dir_a = self.F.direction
            mag_a = self.F.magnitude / self.m
            new_a = Vector(magnitude=mag_a, direction=dir_a)

            # add accelerations
            self.a = add_forces(self.a, new_a)

            # convert calculated acceleration in velocity
            at = Vector(magnitude=(self.a.magnitude * (time.time() - self.time)), direction=self.a.direction)
            self.v = add_forces(self.v, at)

            # move
            self.x += self.v.magnitude * cos(self.v.direction) * (time.time() - self.time)
            self.y += self.v.magnitude * sin(self.v.direction) * (time.time() - self.time)

            # reset forces, accelerations, velocities, TIME (all of them will be 0, except const_forces)
            self.F = self.const_F
            self.v = self.const_v
            self.a = self.const_a
            self.time = time.time()

    def stop(self):
        self.active = False


def create_point(x, y, radius=5.0, mass=1.0, velocity=Vector(magnitude=0.0, direction=0.0), force=Vector(magnitude=0.0, direction=0.0), acceleration=Vector(magnitude=0.0, direction=0.0)):
    points.append(Point(x, y, radius, mass, velocity, force, acceleration))


def setup():
    create_point(100, 100, velocity=Vector(magnitude=100, direction=0.0))
    create_point(100, 200)


def stop():
    global active
    active = False

    for point in points:
        point.stop()
    print("Shut down successfully!")


if __name__ == '__main__':
    setup()

    # make the points alive
    for point in points:
        point.start()

    while active:
        for point in points:
            canvas.coords(point.point, point.x - point.r, point.y - point.r, point.x + point.r, point.y + point.r)

        try:
            canvas.update()
        except tkinter.TclError as e:
            stop()
