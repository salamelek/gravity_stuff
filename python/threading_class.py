from threading import Thread
import tkinter
from math import sqrt, sin, cos, asin, pi
import Exceptions
import time

active = True

# 1px = 1m
canvas_width = 500
canvas_height = 500

G = 6.67430e+04  # e-11

points = []

root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=canvas_height, width=canvas_width, background="black")
# TODO invert the canvas y axis.... No technical improvements but its nicer
canvas.pack()


class Vector:
    def __init__(self, force, direction):
        self.force = force
        self.direction = direction


def add_vectors(vect_a, vect_b):
    a = vect_a
    b = vect_b

    fx = a.force * cos(a.direction) + b.force * cos(b.direction)
    fy = a.force * sin(a.direction) + b.force * sin(b.direction)
    magnitude = sqrt((fx ** 2) + (fy ** 2))

    if magnitude != 0.0:
        direction = asin(fy / magnitude)
        # TODO no work
        if fx < 0 < fy:
            direction = (1 * pi) - direction
        if fy < 0 > fx:
            direction = (1.5 * pi) - direction
        if fy < 0 < fx:
            direction = (2 * pi) - direction
    else:
        # since there is no force, the direction is useless
        direction = 0.0

    return Vector(force=magnitude, direction=direction)


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

                    yb = dist((b.x, self.y), b)
                    f_dir = asin(yb / dist(self, b))
                    if b.x < self.x:
                        f_dir = pi - f_dir

                    self.F = add_vectors(self.F, Vector(force=f_mag, direction=f_dir))

            # convert calculated force to acceleration
            dir_a = self.F.direction
            mag_a = self.F.force / self.m
            new_a = Vector(force=mag_a, direction=dir_a)

            # add accelerations
            self.a = add_vectors(self.a, new_a)

            # convert calculated acceleration in velocity
            at = Vector(force=(self.a.force * (time.time() - self.time)), direction=self.a.direction)
            self.v = add_vectors(self.v, at)

            # move
            self.x += self.v.force * cos(self.v.direction) * (time.time() - self.time)
            self.y += self.v.force * sin(self.v.direction) * (time.time() - self.time)

            # reset forces, accelerations, velocities, TIME (all of them will be 0, except const_forces)
            self.F = self.const_F
            self.v = self.const_v
            self.a = self.const_a
            self.time = time.time()

            time.sleep(1)

    def stop(self):
        self.active = False


def create_point(x, y, radius=10.0, mass=1.0, velocity=Vector(force=0.0, direction=0.0),
                 force=Vector(force=0.0, direction=0.0), acceleration=Vector(force=0.0, direction=0.0)):
    points.append(Point(x, y, radius, mass, velocity, force, acceleration))


def setup():
    create_point(100, 100, velocity=Vector(force=0, direction=0.0))
    create_point(200, 200)


def stop():
    global active
    active = False

    for point in points:
        point.stop()

    root.destroy()
    print("Shut down successfully!")


if __name__ == '__main__':
    setup()
    root.protocol("WM_DELETE_WINDOW", stop)

    # make the points alive
    for point in points:
        point.start()

    while active:
        for point in points:
            # the moveto() moves the top left angle, so we have to subtract r
            canvas.moveto(point.point, point.x - point.r, point.y - point.r)

        canvas.update()
        # TODO the points vibrate, i have no clue why
