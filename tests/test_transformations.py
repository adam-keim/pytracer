from raytracer.base import (
    Point,
    Matrix,
    Translation,
    Vector,
    Scaling,
    RotationX,
    RotationY,
    RotationZ,
    Shearing,
    ViewTransform,
    Identity,
)
import math


def test_translation():
    t = Translation(5, -3, 2)
    p = Point(-3, 4, 5)
    p_exp = Point(2, 1, 7)
    assert t * p == p_exp


def test_inverse_translation():
    t = Translation(5, -3, 2)
    i = t.inverse()
    p = Point(-3, 4, 5)
    assert i * p == Point(-8, 7, 3)


def test_vector_translation():
    t = Translation(5, -3, 2)
    v = Vector(-3, 4, 5)
    assert t * v == v


def test_point_scaling():
    t = Scaling(2, 3, 4)
    p = Point(-4, 6, 8)
    assert t * p == Point(-8, 18, 32)


def test_vector_scaling():
    t = Scaling(2, 3, 4)
    v = Vector(-4, 6, 8)
    assert t * v == Vector(-8, 18, 32)


def test_inverse_scaling():
    t = Scaling(2, 3, 4)
    i = t.inverse()
    v = Vector(-4, 6, 8)
    assert i * v == Vector(-2, 2, 2)


def test_reflection():
    t = Scaling(-1, 1, 1)
    p = Point(2, 3, 4)
    assert t * p == Point(-2, 3, 4)


def test_Xrotation():
    p = Point(0, 1, 0)
    half = RotationX(math.pi / 4)
    full = RotationX(math.pi / 2)
    assert half * p == Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2)
    assert full * p == Point(0, 0, 1)


def test_inv_Xrotation():
    p = Point(0, 1, 0)
    half = RotationX(math.pi / 4)
    inv = half.inverse()
    assert inv * p == Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2)


def test_Yrotation():
    p = Point(0, 0, 1)
    half = RotationY(math.pi / 4)
    full = RotationY(math.pi / 2)
    assert half * p == Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2)
    assert full * p == Point(1, 0, 0)


def test_Zrotation():
    p = Point(0, 1, 0)
    half = RotationZ(math.pi / 4)
    full = RotationZ(math.pi / 2)
    assert half * p == Point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0)
    assert full * p == Point(-1, 0, 0)


def test_xy_shearing():
    p = Point(2, 3, 4)
    s = Shearing(1, 0, 0, 0, 0, 0)
    assert s * p == Point(5, 3, 4)


def test_xz_shearing():
    p = Point(2, 3, 4)
    s = Shearing(0, 1, 0, 0, 0, 0)
    assert s * p == Point(6, 3, 4)


def test_yx_shearing():
    p = Point(2, 3, 4)
    s = Shearing(0, 0, 1, 0, 0, 0)
    assert s * p == Point(2, 5, 4)


def test_yz_shearing():
    p = Point(2, 3, 4)
    s = Shearing(0, 0, 0, 1, 0, 0)
    assert s * p == Point(2, 7, 4)


def test_zx_shearing():
    p = Point(2, 3, 4)
    s = Shearing(0, 0, 0, 0, 1, 0)
    assert s * p == Point(2, 3, 6)


def test_zy_shearing():
    p = Point(2, 3, 4)
    s = Shearing(0, 0, 0, 0, 0, 1)
    print(s * p)
    assert s * p == Point(2, 3, 7)


def test_trans_sequence():
    p = Point(1, 0, 1)
    a = RotationX(math.pi / 2)
    b = Scaling(5, 5, 5)
    c = Translation(10, 5, 7)
    p2 = a * p
    assert p2 == Point(1, -1, 0)
    p3 = b * p2
    assert p3 == Point(5, -5, 0)
    p4 = c * p3
    assert p4 == Point(15, 0, 7)


def test_trans_chaining():
    p = Point(1, 0, 1)
    a = RotationX(math.pi / 2)
    b = Scaling(5, 5, 5)
    c = Translation(10, 5, 7)
    t = c * b * a
    print(t * p)
    assert t * p == Point(15, 0, 7)


def test_default_orientation_matrix():
    f = Point(0, 0, 0)
    to = Point(0, 0, -1)
    up = Vector(0, 1, 0)
    t = ViewTransform(f, to, up)
    print(t)
    assert t == Identity()


def test_positive_z_orientation_matrix():
    f = Point(0, 0, 0)
    to = Point(0, 0, 1)
    up = Vector(0, 1, 0)
    t = ViewTransform(f, to, up)
    print(t)
    assert t == Scaling(-1, 1, -1)


def test_movement():
    f = Point(0, 0, 8)
    to = Point(0, 0, 0)
    up = Vector(0, 1, 0)
    t = ViewTransform(f, to, up)
    assert t == Translation(0, 0, -8)


def test_arbitrary_orientation():
    f = Point(1, 3, 2)
    to = Point(4, -2, 8)
    up = Vector(1, 1, 0)
    t = ViewTransform(f, to, up)
    assert t == Matrix(
        [
            [-0.50709, 0.50709, 0.67612, -2.36643],
            [0.76772, 0.60609, 0.12122, -2.82843],
            [-0.35857, 0.59761, -0.71714, 0.00000],
            [0.00000, 0.00000, 0.00000, 1.00000],
        ]
    )
