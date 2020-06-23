from raytracer.shapes import Sphere, Cube, Plane
from raytracer.base import (
    ViewTransform,
    Point,
    Vector,
    Color,
    Translation,
    Scaling,
    RotationX,
)
from raytracer.lights import PointLight
from raytracer.camera import Camera
from raytracer.materials import Material
from raytracer.world import World
import math
import copy

# cover.yml
# # ======================================================
# # the camera
# # ======================================================
# - add: camera
# width: 100
# height: 100
# field-of-view: 0.785
# from: [ -6, 6, -10 ]
# to: [ 6, 0, 6 ]
# up: [ -0.45, 1, 0 ]
c = Camera(512, 512, 0.785)
c.transform = ViewTransform(Point(-6, 6, -10), Point(6, 0, 6), Vector(-0.45, 1, 0))

# # ======================================================
# # light sources
# # ======================================================
# - add: light
# at: [ 50, 100, -50 ]
# intensity: [ 1, 1, 1 ]
# # an optional second light for additional illumination
light = PointLight(Point(50, 100, -50), Color(1, 1, 1))

# - add: light
# at: [ -400, 50, -10 ]
# intensity: [ 0.2, 0.2, 0.2 ]
# # ======================================================
# # define some constants to avoid duplication
# # ======================================================
# - define: white-material
# value:
# color: [ 1, 1, 1 ]
# diffuse: 0.7
# ambient: 0.1
# specular: 0.0
# reflective: 0.1
white = Material()
white.color = Color(1, 1, 1)
white.diffuse = 0.7
white.ambient = 0.1
white.specular = 0.0
white.reflective = 0.1

# - define: blue-material
# extend: white-material
# value:
# color: [ 0.537, 0.831, 0.914 ]
blue = copy.deepcopy(white)
blue.color = Color(0.537, 0.831, 0.914)

# - define: red-material
# extend: white-material
# value:
# color: [ 0.941, 0.322, 0.388 ]
red = copy.deepcopy(white)
red.color = Color(0.941, 0.322, 0.388)

# - define: purple-material
# extend: white-material
# value:
# color: [ 0.373, 0.404, 0.550 ]
purple = copy.deepcopy(white)
purple.color = Color(0.373, 0.322, 0.388)

# - define: standard-transform
# value:
# - [ translate, 1, -1, 1 ]
# - [ scale, 0.5, 0.5, 0.5 ]
standard = Scaling(0.5, 0.5, 0.5) * Translation(1, -1, 1)

# - define: large-object
# value:
# - standard-transform
# - [ scale, 3.5, 3.5, 3.5 ]
large = Scaling(3.5, 3.5, 3.5) * standard

# - define: medium-object
# value:
# - standard-transform
# - [ scale, 3, 3, 3 ]
medium = Scaling(3, 3, 3) * standard

# - define: small-object
# value:
# - standard-transform
# - [ scale, 2, 2, 2 ]
small = Scaling(2, 2, 2) * standard

# # ======================================================
# # a white backdrop for the scene
# # ======================================================
w = World()
w.light = light

# - add: plane
# material:
# color: [ 1, 1, 1 ]
# ambient: 1
# diffuse: 0
# specular: 0
# transform:
# - [ rotate-x, 1.5707963267948966 ] # pi/2
# - [ translate, 0, 0, 500 ]
p = Plane()
p.material.color = Color(1, 1, 1)
p.material.ambient = 1
p.material.diffuse = 0
p.material.specular = 0
p.set_transform(Translation(0, 0, 500) * RotationX(math.pi / 2))
w.objects.append(p)

# # ======================================================
# # describe the elements of the scene
# # ======================================================
# - add: sphere
# material:
# color: [ 0.373, 0.404, 0.550 ]
# diffuse: 0.2
# ambient: 0.0
# specular: 1.0
# shininess: 200
# reflective: 0.7
# transparency: 0.7
# refractive-index: 1.5
# transform:
# - large-object
s = Sphere()
s.material.color = Color(0.393, 0.404, 0.550)
s.material.diffuse = 0.2
s.material.ambient = 0.0
s.material.specular = 1.0
s.material.shininess = 200
s.material.reflective = 0.7
s.material.transparency = 0.7
s.material.refractive_index = 1.5
s.set_transform(large)
w.objects.append(s)

# - add: cube
# material: white-material
# transform:
# - medium-object
# - [ translate, 4, 0, 0 ]
c1 = Cube()
c1.material = white
c1.set_transform(Translation(4, 0, 0) * medium)
w.objects.append(c1)

# - add: cube
# material: blue-material
# transform:
# - large-object
# - [ translate, 8.5, 1.5, -0.5 ]
c2 = Cube()
c2.material = blue
c2.set_transform(Translation(8.5, 1.5, -0.5) * large)
w.objects.append(c2)

# - add: cube
# material: red-material
# transform:
# - large-object
# - [ translate, 0, 0, 4 ]
c3 = Cube()
c3.material = white
c3.set_transform(Translation(0, 0, 4) * large)
w.objects.append(c3)

# - add: cube
# material: white-material
# transform:
# - small-object
# - [ translate, 4, 0, 4 ]
c4 = Cube()
c4.material = white
c4.set_transform(Translation(4, 0, 4) * small)
w.objects.append(c4)

# - add: cube
# material: purple-material
# transform:
# - medium-object
# - [ translate, 7.5, 0.5, 4 ]
c5 = Cube()
c5.material = purple
c5.set_transform(Translation(7.5, 0.5, 4) * medium)
w.objects.append(c5)

# - add: cube
# material: white-material
# transform:
# - medium-object
# - [ translate, -0.25, 0.25, 8 ]
c6 = Cube()
c6.material = white
c6.set_transform(Translation(-0.25, 0.25, 8) * medium)
w.objects.append(c6)

# - add: cube
# material: blue-material
# transform:
# - large-object
# - [ translate, 4, 1, 7.5 ]
c7 = Cube()
c7.material = blue
c7.set_transform(Translation(4, 1, 7.5) * large)
w.objects.append(c7)

# - add: cube
# material: red-material
# transform:
# - medium-object
# - [ translate, 10, 2, 7.5 ]
c8 = Cube()
c8.material = red
c8.set_transform(Translation(10, 2, 7.5) * medium)
w.objects.append(c8)

# - add: cube
# material: white-material
# transform:
# - small-object
# - [ translate, 8, 2, 12 ]
c9 = Cube()
c9.material = white
c9.set_transform(Translation(8, 2, 12) * small)
w.objects.append(c9)


# - add: cube
# material: white-material
# transform:
# - small-object
# - [ translate, 20, 1, 9 ]
c10 = Cube()
c10.material = white
c10.set_transform(Translation(20, 1, 9) * small)
w.objects.append(c10)

# - add: cube
# material: blue-material
# transform:
# - large-object
# - [ translate, -0.5, -5, 0.25 ]
c11 = Cube()
c11.material = blue
c11.set_transform(Translation(-0.5, -5, 0.25) * large)
w.objects.append(c11)

# - add: cube
# material: red-material
# transform:
# - large-object
# - [ translate, 4, -4, 0 ]
c12 = Cube()
c12.material = red
c12.set_transform(Translation(4, -4, 0) * large)
w.objects.append(c12)

# - add: cube
# material: white-material
# transform:
# - large-object
# - [ translate, 8.5, -4, 0 ]
c13 = Cube()
c13.material = white
c13.set_transform(Translation(8.5, -4, 0) * large)
w.objects.append(c13)

# - add: cube
# material: white-material
# transform:
# - large-object
# - [ translate, 0, -4, 4 ]
c14 = Cube()
c14.material = white
c14.set_transform(Translation(0, -4, 4) * large)
w.objects.append(c14)

# - add: cube
# material: purple-material
# transform:
# - large-object
# - [ translate, -0.5, -4.5, 8 ]
c15 = Cube()
c15.material = purple
c15.set_transform(Translation(-0.5, -4.5, 8) * large)
w.objects.append(c15)

# - add: cube
# material: white-material
# transform:
# - large-object
# - [ translate, 0, -8, 4 ]
c16 = Cube()
c16.material = white
c16.set_transform(Translation(0, -8, 4) * large)
w.objects.append(c16)

# - add: cube
# material: white-material
# transform:
# - large-object
# - [ translate, -0.5, -8.5, 8 ]
c17 = Cube()
c17.material = white
c17.set_transform(Translation(-0.5, -8.5, 8) * large)
w.objects.append(c17)


canvas = c.render(w)
with open("cover2.ppm", "w") as f:
    f.write(canvas.to_ppm())
