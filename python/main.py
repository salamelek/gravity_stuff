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


def dist(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class Point:
    def __init__(self, canvas, x, y, r, vx=0.0, vy=0.0, ax=0.0, ay=0.0, f=0.0, fx=0.0, fy=0.0, mass=1.0, wkx=0.0, wky=0.0):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.f = f
        self.fx = fx
        self.fy = fy
        self.mass = mass
        self.canvas = canvas
        self.wkx = wkx
        self.wky = wky

        self.point = self.canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="red")

    def move_by(self, x, y):
        self.canvas.move(self.point, x, y)

    def delete(self):
        self.canvas.delete(self.point)
        return

    def update(self):
        coords = self.canvas.coords(self.point)

        self.x = (coords[0] + coords[2]) / 2
        self.y = (coords[1] + coords[3]) / 2

        self.ax = self.fx / self.mass
        self.ay = self.fy / self.mass

        self.vx += self.ax
        self.vy += self.ay

        if self.x >= (canvas_width - self.r) or self.x <= (0 + self.r):
            self.vx *= -1

        if self.y >= (canvas_height - self.r) or self.y <= (0 + self.r):
            self.vy *= -1

        # I want these to be directional, so don't boo me
        self.wkx = (self.mass * self.vx ** 2) / 2
        # if self.vx < 0:
        #     self.wkx *= -1
        self.wky = (self.mass * self.vy ** 2) / 2
        # if self.vy < 0:
        #     self.wky *= -1

        self.fx = 0
        self.fy = 0


class Engine:
    def __init__(self):
        self.root = tkinter.Tk()

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.canvas = tkinter.Canvas(self.root, height=self.canvas_height, width=self.canvas_width, background="black")

        self.canvas.pack()

    def update(self):
        points_to_delete = []
        new_points = []

        # interactions
        for i in range(len(points)):
            for j in range(len(points) - (i + 1)):
                a = points[i]
                b = points[j + 1 + i]

                if dist(a, b) > (a.r + b.r):
                    r = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
                    f = G * ((a.mass * b.mass) / r ** 2)
                    a.fx += ((b.x - a.x) * f) / r
                    a.fy += ((b.y - a.y) * f) / r
                    b.fx += ((a.x - b.x) * f) / r
                    b.fy += ((a.y - b.y) * f) / r

                # collision detected
                else:
                    # two become one
                    points_to_delete.append(a)
                    points_to_delete.append(b)

                    r = math.sqrt(a.r ** 2 + b.r ** 2)
                    m = a.mass + b.mass
                    x = (a.x + b.x) / 2
                    y = (a.y + b.y) / 2
                    wkx = a.wkx + b.wkx
                    wky = a.wky + b.wky
                    vx = math.sqrt((2 * wkx) / m)
                    # if (a.vx < 0 and not b.vx < 0) or (not a.vx < 0 and b.vx < 0):
                    #     vx *= -1
                    vy = math.sqrt((2 * wky) / m)
                    # if (a.vy < 0 and not b.vy < 0) or (not a.vy < 0 and b.vy < 0):
                    #     vy *= -1

                    new_points.append((x, y, r, vx, vy, m))

                    # the two bounce
                    # bounce(a, b)

        for point_to_delete in points_to_delete:
            points.remove(point_to_delete)
            point_to_delete.delete()
            del point_to_delete

        for new_point in new_points:
            myEngine.create_point(x=new_point[0], y=new_point[1], r=new_point[2], vx=new_point[3], vy=new_point[4], mass=new_point[5])

        # actions
        for point in points:
            point.update()
            point.move_by(point.vx, point.vy)

        self.canvas.update()

    def create_point(self, x, y, r=10.0, vx=0.0, vy=0.0, ax=0.0, ay=0.0, f=0.0, fx=0.0, fy=0.0, mass=1.0):
        point = Point(canvas=self.canvas, x=x, y=y, r=r, vx=vx, vy=vy, ax=ax, ay=ay, f=f, fx=fx, fy=fy, mass=mass)
        points.append(point)


if __name__ == "__main__":
    # TODO time based simulation, not framerate
    # TODO IMPORTANT change the physics engine to use absolute velocity and DIRECTION

    myEngine = Engine()

    for i in range(5):
        myEngine.create_point(x=random.randint(11, canvas_width - 11), y=random.randint(11, canvas_height - 11))

    # myEngine.create_point(400, 500)
    # myEngine.create_point(600, 500)

    while active:
        myEngine.update()

        target_time = time.time() + refresh_rate
        while time.time() < target_time:
            pass
