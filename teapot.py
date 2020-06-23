from raytracer.parser import Parser
from raytracer.world import World
from raytracer.camera import Camera
from raytracer.lights import PointLight
from raytracer.base import Point, Color, ViewTransform, Vector
f = open("tests/obj_files/face.obj", "r")
p = Parser(f)
w = World()
w.objects.append(p.obj_to_group())
w.light = PointLight(Point(10, 5, 5), Color(1,1,1))
c = Camera(10, 10, 0.785)
c.transform = ViewTransform(Point(-6, 6, -10), Point(6, 0, 6), Vector(-0.45, 1, 0))
canvas = c.render(w)
with open("images/triangl.ppm", "w") as f:
    f.write(canvas.to_ppm())
# This is wayyy too slow we're gonna need a triangle mesh or something