from raytracer.shapes import Cylinder
from raytracer.base import Point, Vector, equal
from raytracer.rays import Ray
import math


def ray_miss_helper(origin, direction):
    c = Cylinder()
    dir = direction.normalize()
    r = Ray(origin, dir)
    xs = c.local_intersect(r)
    assert len(xs) == 0


def test_ray_miss_1():
    ray_miss_helper(Point(1, 0, 0), Vector(0, 1, 0))


def test_ray_miss_2():
    ray_miss_helper(Point(0, 0, 0), Vector(0, 1, 0))


def test_ray_miss_3():
    ray_miss_helper(Point(0, 0, -5), Vector(1, 1, 1))


def ray_hit_helper(origin, direction):
    c = Cylinder()
    dir = direction.normalize()
    r = Ray(origin, dir)
    xs = c.local_intersect(r)
    assert len(xs) == 2
    return (xs[0].t, xs[1].t)


def test_ray_hit_1():
    assert (5, 5) == ray_hit_helper(Point(1, 0, -5), Vector(0, 0, 1))


def test_ray_hit_2():
    assert (4, 6) == ray_hit_helper(Point(0, 0, -5), Vector(0, 0, 1))


def test_ray_hit_3():
    t0, t1 = ray_hit_helper(Point(0.5, 0, -5), Vector(0.1, 1, 1))
    assert equal(6.80798, t0)
    assert equal(7.08872, t1)


def normal_helper(point):
    c = Cylinder()
    n = c.local_normal_at(point)
    return n


def test_normal_1():
    assert Vector(1, 0, 0) == normal_helper(Point(1, 0, 0))


def test_normal_2():
    assert Vector(0, 0, -1) == normal_helper(Point(0, 5, -1))


def test_normal_3():
    assert Vector(0, 0, 1) == normal_helper(Point(0, -2, 1))


def test_normal_4():
    assert Vector(-1, 0, 0) == normal_helper(Point(-1, 1, 0))


def test_min_max_bounds():
    c = Cylinder()
    assert c.minimum == -math.inf
    assert c.maximum == math.inf


def constrained_cylinder_helper(point, direction) -> int:
    c = Cylinder()
    c.minimum = 1
    c.maximum = 2
    dir = direction.normalize()
    r = Ray(point, dir)
    xs = c.local_intersect(r)
    return len(xs)


def test_constrained_intersect_1():
    assert 0 == constrained_cylinder_helper(Point(0, 1.5, 0), Vector(0.1, 1, 0))


def test_constrained_intersect_2():
    assert 0 == constrained_cylinder_helper(Point(0, 3, -5), Vector(0, 0, 1))


def test_constrained_intersect_3():
    assert 0 == constrained_cylinder_helper(Point(0, 0, -5), Vector(0, 0, 1))


def test_constrained_intersect_4():
    assert 0 == constrained_cylinder_helper(Point(0, 2, -5), Vector(0, 0, 1))


def test_constrained_intersect_5():
    assert 0 == constrained_cylinder_helper(Point(0, 1, -5), Vector(0, 0, 1))


def test_constrained_intersect_6():
    assert 2 == constrained_cylinder_helper(Point(0, 1.5, -2), Vector(0, 0, 1))


def test_default_closed():
    c = Cylinder()
    assert c.closed == False


def closed_intersect_helper(origin, direction):
    c = Cylinder()
    c.minimum = 1
    c.maximum = 2
    c.closed = True
    dir = direction.normalize()
    r = Ray(origin, dir)
    xs = c.local_intersect(r)
    return len(xs)


def test_closed_intersect_1():
    assert closed_intersect_helper(Point(0, 3, 0), Vector(0, -1, 0)) == 2


def test_closed_intersect_2():
    assert closed_intersect_helper(Point(0, 3, -2), Vector(0, -1, 2)) == 2


def test_closed_intersect_3():
    assert closed_intersect_helper(Point(0, 4, -2), Vector(0, -1, 1)) == 2


def test_closed_intersect_4():
    assert closed_intersect_helper(Point(0, 0, -2), Vector(0, 1, 2)) == 2


def test_closed_intersect_5():
    assert closed_intersect_helper(Point(0, -1, -2), Vector(0, 1, 1)) == 2


def end_normal_helper(point):
    c = Cylinder()
    c.minimum = 1
    c.maximum = 2
    c.closed = True
    n = c.local_normal_at(point)
    return n


def test_end_normal_1():
    assert end_normal_helper(Point(0, 1, 0)) == Vector(0, -1, 0)


def test_end_normal_2():
    assert end_normal_helper(Point(0.5, 1, 0)) == Vector(0, -1, 0)


def test_end_normal_3():
    assert end_normal_helper(Point(0, 1, 0.5)) == Vector(0, -1, 0)


def test_end_normal_4():
    assert end_normal_helper(Point(0, 2, 0)) == Vector(0, 1, 0)


def test_end_normal_5():
    assert end_normal_helper(Point(0.5, 2, 0)) == Vector(0, 1, 0)


def test_end_normal_6():
    assert end_normal_helper(Point(0, 2, 0.5)) == Vector(0, 1, 0)
