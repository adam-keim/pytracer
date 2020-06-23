from raytracer.camera import Camera
from raytracer.base import (
    Identity,
    equal,
    Point,
    Vector,
    RotationY,
    Translation,
    ViewTransform,
    Color,
)
from raytracer.world import World
import math


def test_camera_attributes():
    hsize = 160
    vsize = 120
    fov = math.pi / 2
    c = Camera(hsize, vsize, fov)
    assert c.hsize == 160
    assert c.vsize == 120
    assert c.fov == math.pi / 2
    assert c.transform == Identity()


def test_h_pixel_size():
    c = Camera(200, 125, math.pi / 2)
    assert equal(c.pixel_size, 0.01)


def test_v_pixel_size():
    c = Camera(125, 200, math.pi / 2)
    assert equal(c.pixel_size, 0.01)


def test_center_canvas_ray():
    c = Camera(201, 101, math.pi / 2)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == Point(0, 0, 0)
    assert r.direction == Vector(0, 0, -1)


def test_corner_canvas_ray():
    c = Camera(201, 101, math.pi / 2)
    r = c.ray_for_pixel(0, 0)
    assert r.origin == Point(0, 0, 0)
    assert r.direction == Vector(0.66519, 0.33259, -0.66851)


def test_camera_transform_ray():
    c = Camera(201, 101, math.pi / 2)
    c.transform = RotationY(math.pi / 4) * Translation(0, -2, 5)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == Point(0, 2, -5)
    print(r.direction)
    assert r.direction == Vector(math.sqrt(2) / 2, 0, -math.sqrt(2) / 2)


def test_render():
    w = World.default()
    c = Camera(11, 11, math.pi / 2)
    f = Point(0, 0, -5)
    to = Point(0, 0, 0)
    up = Vector(0, 1, 0)
    c.transform = ViewTransform(f, to, up)
    image = c.render(w)
    assert image.read_pixel(5, 5) == Color(0.38066, 0.47583, 0.2855)
