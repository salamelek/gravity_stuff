from threading import Thread
import tkinter
from math import sqrt, sin, cos, asin, pi
import Exceptions
import time

G = 6.67430e+04  # e-11


class Vector:
    def __init__(self, force, direction):
        self.force = force
        self.direction = direction

    def print_self(self):
        print("===========[printing vector]============")
        print(f"Force: {self.force} N\nDirection: {self.direction * (180 / pi)} DEG | {self.direction} RAD")
        print("===========[printing vector]============")


def add_vectors(vect_a, vect_b):
    a = vect_a
    b = vect_b

    fx = a.force * cos(a.direction) + b.force * cos(b.direction)
    print(fx)
    fy = a.force * sin(a.direction) + b.force * sin(b.direction)
    print(fy)
    magnitude = sqrt((fx ** 2) + (fy ** 2))

    if magnitude != 0.0:
        direction = asin(fy / magnitude)

        # there are 4 quadrants
        if fx < 0:
            direction = pi - direction

    else:
        # since there is no force, the direction is useless
        direction = 0.0

    return Vector(force=magnitude, direction=direction)


if __name__ == '__main__':
    a = Vector(1, 1/4 * pi)
    # b = Vector(1, 2.356194490192345)
    b = Vector(1, 5/4 * pi)
    c = add_vectors(a, b)
    c.print_self()
