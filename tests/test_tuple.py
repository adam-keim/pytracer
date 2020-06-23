from raytracer.base import Tuple, Point, Vector, equal
import math

# TEST TUPLES
def test_point_tuple():
    t = Tuple(4.3, -4.2, 3.1, 1.0)
    assert t.x == 4.3
    assert t.y == -4.2
    assert t.z == 3.1
    assert t.w == 1.0
    assert t.isVector() == False
    assert t.isPoint() == True


def test_vector_tuple():
    t = Tuple(4.3, -4.2, 3.1, 0.0)
    assert t.x == 4.3
    assert t.y == -4.2
    assert t.z == 3.1
    assert t.w == 0.0
    assert t.isVector() == True
    assert t.isPoint() == False


def test_point():
    p = Point(4, -4, 3)
    t = Tuple(4, -4, 3, 1)
    assert p.isPoint() == True
    assert p == t


def test_vector():
    v = Vector(4, -4, 3)
    t = Tuple(4, -4, 3, 0)
    assert v.isVector() == True
    assert v == t


def test_add_tuples():
    a1 = Tuple(3, -2, 5, 1)
    a2 = Tuple(-2, 3, 1, 0)
    assert a1 + a2 == Tuple(1, 1, 6, 1)


def test_sub_points():
    p1 = Point(3, 2, 1)
    p2 = Point(5, 6, 7)
    assert p1 - p2 == Vector(-2, -4, -6)


def test_sub_vector_point():
    p = Point(3, 2, 1)
    v = Vector(5, 6, 7)
    assert p - v == Point(-2, -4, -6)


def test_sub_vectors():
    v1 = Vector(3, 2, 1)
    v2 = Vector(5, 6, 7)
    assert v1 - v2 == Vector(-2, -4, -6)


def test_zero_sub():
    zero = Vector(0, 0, 0)
    v = Vector(1, -2, 3)
    assert zero - v == Vector(-1, 2, -3)


def test_neg():
    a = Tuple(1, -2, 3, -4)
    assert -a == Tuple(-1, 2, -3, 4)


def test_mult_scalar():
    a = Tuple(1, -2, 3, -4)
    assert a * 3.5 == Tuple(3.5, -7, 10.5, -14)


def test_mult_fraction():
    a = Tuple(1, -2, 3, -4)
    assert a * 0.5 == Tuple(0.5, -1, 1.5, -2)


def test_division():
    a = Tuple(1, -2, 3, -4)
    assert a / 2 == Tuple(0.5, -1, 1.5, -2)


def test_magnitudes():
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    v3 = Vector(0, 0, 1)
    v4 = Vector(1, 2, 3)
    v5 = Vector(-1, -2, -3)
    assert v1.magnitude() == 1
    assert v2.magnitude() == 1
    assert v3.magnitude() == 1
    assert v4.magnitude() == math.sqrt(14)
    assert v5.magnitude() == math.sqrt(14)


def test_normalize():
    v1 = Vector(4, 0, 0)
    v2 = Vector(1, 2, 3)
    assert v1.normalize() == Vector(1, 0, 0)
    assert v2.normalize() == Vector(0.26726, 0.53452, 0.80178)
    assert v2.normalize().magnitude() == 1


def test_dot():
    v1 = Vector(1, 2, 3)
    v2 = Vector(2, 3, 4)
    assert v1.dot(v2) == 20


def test_cross():
    v1 = Vector(1, 2, 3)
    v2 = Vector(2, 3, 4)
    assert v1.cross(v2) == Vector(-1, 2, -1)
    assert v2.cross(v1) == Vector(1, -2, 1)


def test_reflect_45():
    v = Vector(1, -1, 0)
    n = Vector(0, 1, 0)
    r = v.reflect(n)
    assert r == Vector(1, 1, 0)


def test_reflect_slanted():
    v = Vector(0, -1, 0)
    n = Vector(math.sqrt(2) / 2, math.sqrt(2) / 2, 0)
    r = v.reflect(n)
    assert r == Vector(1, 0, 0)
