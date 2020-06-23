from raytracer.shapes import Cone
from raytracer.rays import Ray
from raytracer.base import Point, Color, equal, Vector
import math


def cone_ray_helper(origin, direction):
    s = Cone()
    dir = direction.normalize()
    r = Ray(origin, dir)
    xs = s.local_intersect(r)
    assert len(xs) == 2
    return (xs[0].t, xs[1].t)


def test_cone_ray_1():
    t0, t1 = cone_ray_helper(Point(0, 0, -5), Vector(0, 0, 1))
    assert t0 == 5
    assert t1 == 5


def test_cone_ray_2():
    t0, t1 = cone_ray_helper(Point(0, 0, -5), Vector(1, 1, 1))
    assert equal(t0, 8.66025)
    assert equal(t1, 8.66025)


def test_cone_ray_3():
    t0, t1 = cone_ray_helper(Point(1, 1, -5), Vector(-0.5, -1, 1))
    assert equal(t0, 4.55006)
    assert equal(t1, 49.44994)


def test_cone_parallel_ray():
    s = Cone()
    direction = Vector(0, 1, 1).normalize()
    r = Ray(Point(0, 0, -1), direction)
    xs = s.local_intersect(r)
    assert len(xs) == 1
    assert equal(xs[0].t, 0.35355)


def intersect_end_caps_helper(origin, direction):
    s = Cone()
    s.minimum = -0.5
    s.maximum = 0.5
    s.closed = True
    dir = direction.normalize()
    r = Ray(origin, dir)
    xs = s.local_intersect(r)
    return len(xs)


def test_intersect_end_caps_1():
    assert intersect_end_caps_helper(Point(0, 0, -5), Vector(0, 1, 0)) == 0


def test_intersect_end_caps_2():
    assert intersect_end_caps_helper(Point(0, 0, -0.25), Vector(0, 1, 1)) == 2


def test_intersect_end_caps_3():
    assert intersect_end_caps_helper(Point(0, 0, -0.25), Vector(0, 1, 0)) == 4


def normal_helper(point):
    s = Cone()
    n = s.local_normal_at(point)
    return n


def test_cone_normal_1():
    assert normal_helper(Point(0, 0, 0)) == Vector(0, 0, 0)


def test_cone_normal_2():
    assert normal_helper(Point(1, 1, 1)) == Vector(1, -math.sqrt(2), 1)


def test_cone_normal_3():
    assert normal_helper(Point(-1, -1, 0)) == Vector(-1, 1, 0)
