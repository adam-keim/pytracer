from raytracer import base
from typing import NamedTuple


class World:
    def __init__(self, g: base.Vector, w: base.Vector):
        self.gravity = g
        self.wind = w


class Projectile:
    def __init__(self, p, v):
        self.position = p
        self.velocity = v


def tick(w: World, p: Projectile) -> Projectile:
    pos = p.position + p.velocity
    velocity = p.velocity + w.gravity + w.wind
    return Projectile(pos, velocity)


start = base.Point(0, 1, 0)
velocity = base.Vector(1, 1.8, 0).normalize() * 11.25
p = Projectile(start, velocity)
gravity = base.Vector(0, -0.1, 0)
wind = base.Vector(-0.01, 0, 0)
w = World(gravity, wind)
c = base.Canvas(900, 550)
c1 = base.Color(1, 0, 0)
t = 0
while p.position.y > 0:
    c.write_pixel(int(p.position.x), 550 - int(p.position.y), c1)
    p = tick(w, p)
    t += 1

with open("image.ppm", "w") as f:
    f.write(c.to_ppm())
