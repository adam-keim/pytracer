from raytracer.shapes import Cube
from raytracer.base import Vector, Point
from raytracer.rays import Ray


def cube_intersect_helper(origin, direction, t1, t2):
    c = Cube()
    r = Ray(origin, direction)
    xs = c.local_intersect(r)
    assert len(xs) == 2
    assert xs[0].t == t1
    assert xs[1].t == t2


def test_cube_intersect_posx():
    cube_intersect_helper(Point(5, 0.5, 0), Vector(-1, 0, 0), 4, 6)


def test_cube_intersect_negx():
    cube_intersect_helper(Point(-5, 0.5, 0), Vector(1, 0, 0), 4, 6)


def test_cube_intersect_posy():
    cube_intersect_helper(Point(0.5, 5, 0), Vector(0, -1, 0), 4, 6)


def test_cube_intersect_negy():
    cube_intersect_helper(Point(0.5, -5, 0), Vector(0, 1, 0), 4, 6)


def test_cube_intersect_posz():
    cube_intersect_helper(Point(0.5, 0, 5), Vector(0, 0, -1), 4, 6)


def test_cube_intersect_negz():
    cube_intersect_helper(Point(0.5, 0, -5), Vector(0, 0, 1), 4, 6)


def test_cube_intersect_inside():
    cube_intersect_helper(Point(0, 0.5, 0), Vector(0, 0, 1), -1, 1)


def cube_miss_helper(origin, direction):
    c = Cube()
    r = Ray(origin, direction)
    xs = c.local_intersect(r)
    assert len(xs) == 0


def test_cube_miss_1():
    cube_miss_helper(Point(-2, 0, 0), Vector(0.2673, 0.5345, 0.8018))


def test_cube_miss_2():
    cube_miss_helper(Point(0, -2, 0), Vector(0.8018, 0.2673, 0.5345))


def test_cube_miss_3():
    cube_miss_helper(Point(0, 0, -2), Vector(0.5345, 0.8018, 0.2673))


def test_cube_miss_4():
    cube_miss_helper(Point(2, 0, 2), Vector(0, 0, -1))


def test_cube_miss_5():
    cube_miss_helper(Point(0, 2, 2), Vector(0, -1, 0))


def test_cube_miss_6():
    cube_miss_helper(Point(2, 2, 0), Vector(-1, 0, 0))


def cube_normal_helper(point, normal_exp):
    c = Cube()
    p = point
    normal = c.local_normal_at(p)
    assert normal == normal_exp


def test_cube_normal_1():
    cube_normal_helper(Point(1, 0.5, -0.8), Vector(1, 0, 0))


def test_cube_normal_2():
    cube_normal_helper(Point(-1, -0.2, 0.9), Vector(-1, 0, 0))


def test_cube_normal_3():
    cube_normal_helper(Point(-0.4, 1, -0.1), Vector(0, 1, 0))


def test_cube_normal_4():
    cube_normal_helper(Point(0.3, -1, -0.7), Vector(0, -1, 0))


def test_cube_normal_5():
    cube_normal_helper(Point(-0.6, 0.3, 1), Vector(0, 0, 1))


def test_cube_normal_6():
    cube_normal_helper(Point(0.4, 0.4, -1), Vector(0, 0, -1))


def test_cube_normal_7():
    cube_normal_helper(Point(1, 1, 1), Vector(1, 0, 0))


def test_cube_normal_8():
    cube_normal_helper(Point(-1, -1, -1), Vector(-1, 0, 0))
