from raytracer.shapes import Sphere, Plane, GlassSphere
from raytracer.base import (
    RotationX,
    RotationY,
    RotationZ,
    Translation,
    Scaling,
    Color,
    Point,
    ViewTransform,
    Vector,
)
from raytracer.patterns import CheckersPattern, StripePattern
from raytracer.lights import PointLight
from raytracer.camera import Camera
from raytracer.world import World
import math


floor = Plane()
floor.material.color = Color(1.0, 0.9, 0.9)
floor.material.pattern = CheckersPattern(Color(1, 1, 1), Color(0, 0, 0))
floor.material.reflective = 0.5
floor.material.specular = 0


middle = Sphere()
middle.set_transform(Translation(-0.5, 1, 0.5))
middle.material.transparency = 0.9
middle.material.diffuse = 0.1
middle.material.reflective = 0.9
middle.material.refractive_index = 1.5
middle.material.specular = 1
middle.material.shininess = 300

right = Sphere()
right.set_transform(Translation(1.5, 0.5, -0.5) * Scaling(0.5, 1, 0.5))
right.material.pattern = StripePattern(Color(1, 1, 1), Color(0, 1, 0))
right.material.pattern.set_pattern_transform(
    Scaling(0.1, 0.1, 0.1) * RotationY(math.pi / 4)
)
right.material.color = Color(0.1, 1, 0.5)
right.material.diffuse = 0.7
right.material.specular = 0.3

left = Sphere()
left.transform = Translation(-1.5, 0.33, -0.75) * Scaling(0.33, 0.33, 0.33)
left.material.color = Color(1, 0.8, 0.1)
left.material.diffuse = 0.7
left.material.specular = 0.3

world = World()
world.objects.extend([floor, middle, right, left])
world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

camera = Camera(1024, 512, math.pi / 3)
camera.transform = ViewTransform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))

canvas = camera.render(world)
with open("pattern.ppm", "w") as f:
    f.write(canvas.to_ppm())
