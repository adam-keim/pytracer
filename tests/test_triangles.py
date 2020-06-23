from raytracer.shapes import Triangle
from raytracer.base import Point, Vector
from raytracer.rays import Ray


def test_triangle_creation():
    p1 = Point(0, 1, 0)
    p2 = Point(-1, 0, 0)
    p3 = Point(1, 0, 0)
    t = Triangle(p1, p2, p3)
    assert t.p1 == p1
    assert t.p2 == p2
    assert t.p3 == p3
    assert t.e1 == Vector(-1, -1, 0)
    assert t.e2 == Vector(1, -1, 0)
    assert t.normal == Vector(0, 0, -1)


def test_triangle_normal():
    t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
    n1 = t.local_normal_at(Point(0, 0.5, 0))
    n2 = t.local_normal_at(Point(-0.5, 0.75, 0))
    n3 = t.local_normal_at(Point(0.5, 0.25, 0))
    assert n1 == t.normal
    assert n2 == t.normal
    assert n3 == t.normal


def test_parallel_miss():
    t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
    r = Ray(Point(0, -1, -2), Vector(0, 1, 0))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def test_p1_p3_miss():
    t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
    r = Ray(Point(1, 1, -2), Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def test_p1_p2_miss():
    t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
    r = Ray(Point(-1, 1, -2), Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def test_p2_p3_miss():
    t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
    r = Ray(Point(0, -1, -2), Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def test_ray_hit():
    t = Triangle(Point(0, 1, 0), Point(-1, 0, 0), Point(1, 0, 0))
    r = Ray(Point(0, 0.5, -2), Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 2
