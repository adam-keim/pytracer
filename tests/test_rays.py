from raytracer.rays import Ray, Intersection, Intersections
from raytracer.base import Tuple, Vector, Point, Translation, Scaling, Identity


def test_ray_creation():
    o = Point(1, 2, 3)
    d = Vector(4, 5, 6)
    r = Ray(o, d)
    assert r.origin == o
    assert r.direction == d


def test_ray_position():
    r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
    assert r.position(0) == Point(2, 3, 4)
    assert r.position(1) == Point(3, 3, 4)
    assert r.position(-1) == Point(1, 3, 4)
    assert r.position(2.5) == Point(4.5, 3, 4)


def test_ray_translation():
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = Translation(3, 4, 5)
    r2 = r.transform(m)
    print(r2.origin)
    assert r2.origin == Point(4, 6, 8)
    assert r2.direction == Vector(0, 1, 0)


def test_ray_scaling():
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = Scaling(2, 3, 4)
    r2 = r.transform(m)
    assert r2.origin == Point(2, 6, 12)
    assert r2.direction == Vector(0, 3, 0)
