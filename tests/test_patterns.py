from raytracer.base import Color
from raytracer.patterns import (
    StripePattern,
    _TestPattern,
    GradientPattern,
    RingPattern,
    CheckersPattern,
)
from raytracer.base import Point, Scaling, Translation, Identity
from raytracer.shapes import Sphere

black = Color(0, 0, 0)
white = Color(1, 1, 1)


def test_stripe_pattern():
    pattern = StripePattern(white, black)
    assert pattern.a == white
    assert pattern.b == black


def test_stripe_x():
    pattern = StripePattern(white, black)
    assert pattern.pattern_at(Point(0, 0, 0)) == white
    assert pattern.pattern_at(Point(0.9, 0, 0)) == white
    assert pattern.pattern_at(Point(1, 0, 0)) == black
    assert pattern.pattern_at(Point(-0.1, 0, 0)) == black
    assert pattern.pattern_at(Point(-1, 0, 0)) == black
    assert pattern.pattern_at(Point(-1.1, 0, 0)) == white


def test_stripe_y():
    pattern = StripePattern(white, black)
    assert pattern.pattern_at(Point(0, 0, 0)) == white
    assert pattern.pattern_at(Point(0, 1, 0)) == white
    assert pattern.pattern_at(Point(0, 2, 0)) == white


def test_stripe_z():
    pattern = StripePattern(white, black)
    assert pattern.pattern_at(Point(0, 0, 0)) == white
    assert pattern.pattern_at(Point(0, 0, 1)) == white
    assert pattern.pattern_at(Point(0, 0, 2)) == white


def test_default_transform():
    pattern = _TestPattern()
    assert pattern.transform == Identity()


def test_assign_transform():
    pattern = _TestPattern()
    pattern.set_pattern_transform(Translation(1, 2, 3))
    assert pattern.transform == Translation(1, 2, 3)


def test_object_transform():
    s = Sphere()
    s.set_transform(Scaling(2, 2, 2))
    pattern = _TestPattern()
    c = pattern.pattern_at_shape(s, Point(2, 3, 4))
    assert c == Color(1, 1.5, 2)


def test_pattern_transform():
    s = Sphere()
    p = _TestPattern()
    p.set_pattern_transform(Scaling(2, 2, 2))
    c = p.pattern_at_shape(s, Point(2, 3, 4))
    assert c == Color(1, 1.5, 2)


def test_both_transform():
    s = Sphere()
    s.set_transform(Scaling(2, 2, 2))
    pattern = _TestPattern()
    pattern.set_pattern_transform(Translation(0.5, 1, 1.5))
    c = pattern.pattern_at_shape(s, Point(2.5, 3, 3.5))
    assert c == Color(0.75, 0.5, 0.25)


def test_gradient_pattern():
    p = GradientPattern(white, black)
    assert p.pattern_at(Point(0, 0, 0)) == white
    assert p.pattern_at(Point(0.25, 0, 0)) == Color(0.75, 0.75, 0.75)
    assert p.pattern_at(Point(0.5, 0, 0)) == Color(0.5, 0.5, 0.5)
    assert p.pattern_at(Point(0.75, 0, 0)) == Color(0.25, 0.25, 0.25)


def test_ring_pattern():
    p = RingPattern(white, black)
    assert p.pattern_at(Point(0, 0, 0)) == white
    assert p.pattern_at(Point(1, 0, 0)) == black
    assert p.pattern_at(Point(0, 0, 1)) == black
    # 0.708 = just slightly more than √2/2
    assert p.pattern_at(Point(0.708, 0, 0.708)) == black


def test_checker_x():
    p = CheckersPattern(white, black)
    assert p.pattern_at(Point(0, 0, 0)) == white
    assert p.pattern_at(Point(0.99, 0, 0)) == white
    assert p.pattern_at(Point(1.01, 0, 0)) == black


def test_checker_y():
    p = CheckersPattern(white, black)
    assert p.pattern_at(Point(0, 0, 0)) == white
    assert p.pattern_at(Point(0, 0.99, 0)) == white
    assert p.pattern_at(Point(0, 1.01, 0)) == black


def test_checker_z():
    p = CheckersPattern(white, black)
    assert p.pattern_at(Point(0, 0, 0)) == white
    assert p.pattern_at(Point(0, 0, 0.99)) == white
    assert p.pattern_at(Point(0, 0, 1.01)) == black
