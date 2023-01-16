import pygame
from threading import Thread
from math import pi, sin, asin, sqrt, cos, atan
import time

import Exceptions

pygame.init()

active = True
target_fps = 144
ups = 10000
width = 1200
height = 1200
bcg_color = "black"
objects = []
G = 6.67430-11


class Vector:
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction

    def print_self(self):
        print("=======================")
        print(f"Force: {self.magnitude} N\nDirection: {self.direction * (180 / pi)} DEG | {self.direction} RAD")
        print("=======================")


class Ball(Thread):
    def __init__(self, x, y, radius, velocity, mass, force):
        Thread.__init__(self)

        self.x = x
        self.y = y
        self.m = mass
        self.F = force
        self.r = radius
        self.v = velocity
        self.a = Vector(0, 0)
        self.time = time.time()

        self.active = True

    def update(self):
        self.time = time.time()

    def calc_interactions(self):
        temporary_vectors = []
        final_vector = Vector(0, 0)
        for b in objects:
            if b != self:
                # add up all the forces
                magnitude = G * ((self.m * b.m) / (dist(self, b) ** 2))

                if self.x != b.x:
                    direction = atan((self.y - b.y)/(self.x - b.x))
                    if self.x < b.x:
                        direction += pi

                else:
                    direction = atan((self.x - b.x) / (self.y - b.y))
                    if self.y < b.y:
                        direction += pi

                # this is just temporary and should work only for 2 points. To make definitive, maybe make a list of vectors
                temporary_vectors.append(Vector(magnitude, direction))

        for vector in temporary_vectors:
            final_vector = add_vectors(final_vector, vector)

        self.F = final_vector

    def calc_actions(self):
        acceleration_magnitude = self.F.magnitude / self.m
        acceleration_direction = self.F.direction
        new_acceleration = Vector(magnitude=acceleration_magnitude, direction=acceleration_direction)

        # assign new acceleration
        self.a = new_acceleration

        # convert accelerations to velocities
        velocity_magnitude = self.a.magnitude * (time.time() - self.time)
        velocity_direction = self.a.direction
        new_velocity = Vector(magnitude=velocity_magnitude, direction=velocity_direction)

        # add new velocity
        self.v = add_vectors(self.v, new_velocity)

        # move
        self.x += self.v.magnitude * cos(self.v.direction) * (time.time() - self.time)
        self.y += self.v.magnitude * sin(self.v.direction) * (time.time() - self.time)

    def run(self) -> None:
        print("point running")
        while self.active:
            start_time = time.monotonic()

            self.calc_interactions()
            self.calc_actions()
            self.update()

            end_time = time.monotonic()
            elapsed_time = end_time - start_time
            if elapsed_time < 1/ups:
                time.sleep(1/ups - elapsed_time)

    def stop(self):
        print("point stopping")
        self.active = False


class Renderer(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.screen = pygame.display.set_mode((width, height))
        self.active = True
        self.background_color = bcg_color
        self.target_fps = target_fps
        pygame.display.set_caption("Moving Ball")
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        print("renderer running")
        while self.active:
            self.screen.fill(self.background_color)

            for object in objects:
                pygame.draw.circle(self.screen, "red", (object.x, object.y), object.r, 0)

            pygame.display.flip()
            self.clock.tick(self.target_fps)

    def stop(self):
        print("renderer stopping")
        self.active = False


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


def create_point(x, y, radius=5, velocity=Vector(magnitude=0, direction=0), mass=1.0, force=Vector(magnitude=0.0, direction=0.0)):
    objects.append(Ball(x, y, radius, velocity, mass, force))


def setup():
    create_point(500, 700, mass=1000, velocity=Vector(5, 0))
    create_point(700, 500, mass=1000, velocity=Vector(5, pi))
    create_point(500, 500, mass=1000, velocity=Vector(5, 1/2*pi))
    create_point(700, 700, mass=1000, velocity=Vector(5, -1/2*pi))

    for object in objects:
        object.start()


if __name__ == '__main__':
    def quit():
        global active
        active = False
        renderer.stop()
        for object in objects:
            object.stop()

    renderer = Renderer()
    renderer.start()

    setup()
    begin = time.time()
    while active:
        if objects[0].x >= width:
            print(time.time() - begin)
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
