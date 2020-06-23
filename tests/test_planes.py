from raytracer.shapes import Plane
from raytracer.rays import Ray
from raytracer.base import Vector, Point


def test_constant_normal():
    p = Plane()
    n1 = p.local_normal_at(Point(0, 0, 0))
    n2 = p.local_normal_at(Point(10, 0, -10))
    n3 = p.local_normal_at(Point(-5, 0, 150))
    assert n1 == Vector(0, 1, 0)
    assert n2 == Vector(0, 1, 0)
    assert n3 == Vector(0, 1, 0)


def test_parallel_ray():
    p = Plane()
    r = Ray(Point(0, 10, 0), Vector(0, 0, 1))
    xs = p.local_intersect(r)
    assert len(xs) == 0


def test_coplanar_ray():
    p = Plane()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = p.local_intersect(r)
    assert len(xs) == 0


def test_ray_from_above():
    p = Plane()
    r = Ray(Point(0, 1, 0), Vector(0, -1, 0))
    xs = p.local_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].object == p


def test_ray_from_below():
    p = Plane()
    r = Ray(Point(0, -1, 0), Vector(0, 1, 0))
    xs = p.local_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].object == p
