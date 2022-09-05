import tkinter
import time
import random
import math

active = True
refresh_rate = 0
canvas_width = 1000
canvas_height = 1000
G = 6.67430e-3

points = []


class Point:
    def __init__(self, canvas, x, y, r, vx=0.0, vy=0.0, ax=0.0, ay=0.0, f=0.0, fx=0.0, fy=0.0, mass=1.0):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.F = f
        self.Fx = fx
        self.Fy = fy
        self.mass = mass
        self.canvas = canvas

        self.point = self.canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="red")

    def move_by(self, x, y):
        self.canvas.move(self.point, x, y)

    def update(self):
        coords = self.canvas.coords(self.point)

        self.x = (coords[0] + coords[2]) / 2
        self.y = (coords[1] + coords[3]) / 2

        self.ax = self.Fx / self.mass
        self.ay = self.Fy / self.mass

        self.vx += self.ax
        self.vy += self.ay

        self.Fx = 0
        self.Fy = 0


class Engine:
    def __init__(self):
        self.root = tkinter.Tk()

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.canvas = tkinter.Canvas(self.root, height=self.canvas_height, width=self.canvas_width, background="black")

        self.canvas.pack()

    def update(self):
        for i in range(len(points)):
            for j in range(len(points) - (i + 1)):
                a = points[i]
                b = points[j + 1 + i]

                r = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
                f = G * ((a.mass * b.mass) / r ** 2)
                a.Fx += ((b.x - a.x) * f) / r
                a.Fy += ((b.y - a.y) * f) / r
                b.Fx += ((a.x - b.x) * f) / r
                b.Fy += ((a.y - b.y) * f) / r

        for point in points:
            point.update()
            point.move_by(point.vx, point.vy)

        self.canvas.update()

    def create_point(self, x, y, r=3, vx=0.0, vy=0.0, ax=0.0, ay=0.0, f=0.0, fx=0.0, fy=0.0, mass=1.0):
        point = Point(canvas=self.canvas, x=x, y=y, r=r, vx=vx, vy=vy, ax=ax, ay=ay, f=f, fx=fx, fy=fy, mass=mass)
        points.append(point)


if __name__ == "__main__":
    myEngine = Engine()

    for i in range(5):
        myEngine.create_point(x=random.randint(0, canvas_width), y=random.randint(0, canvas_height))

    while active:
        myEngine.update()

        target_time = time.time() + refresh_rate
        while time.time() < target_time:
            pass
