from raytracer.rays import Intersection, Intersections, Ray
from raytracer.shapes import Sphere, Plane, GlassSphere
from raytracer.base import Point, Vector, Scaling, Translation, EPSILON, equal
import math


def test_intersection_creation():
    s = Sphere()
    i = Intersection(3.5, s)
    assert i.t == 3.5
    assert i.object == s


def test_aggregate_intersections():
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i1, i2)
    assert len(xs) == 2
    assert xs[0].t == 1
    assert xs[1].t == 2


def test_positive_hit():
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i1, i2)
    i = xs.hit()
    assert i == i1


def test_mixed_hit():
    s = Sphere()
    i1 = Intersection(-1, s)
    i2 = Intersection(1, s)
    xs = Intersections(i1, i2)
    i = xs.hit()
    assert i == i2


def test_negative_hit():
    s = Sphere()
    i1 = Intersection(-2, s)
    i2 = Intersection(-1, s)
    xs = Intersections(i1, i2)
    i = xs.hit()
    assert i is None


def test_assert_lowest_hit():
    s = Sphere()
    i1 = Intersection(5, s)
    i2 = Intersection(7, s)
    i3 = Intersection(-3, s)
    i4 = Intersection(2, s)
    xs = Intersections(i1, i2, i3, i4)
    i = xs.hit()
    assert i == i4


def test_precompute_state():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computation(r)
    assert comps.t == i.t
    assert comps.object == i.object
    assert comps.point == Point(0, 0, -1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.normalv == Vector(0, 0, -1)


def test_outside_hit():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computation(r)
    assert comps.inside == False


def test_inside_hit():
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = i.prepare_computation(r)

    assert comps.point == Point(0, 0, 1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.inside == True
    assert comps.normalv == Vector(0, 0, -1)


def test_reflection_vector():
    s = Plane()
    r = Ray(Point(0, 1, -1), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), s)
    comps = i.prepare_computation(r)
    assert comps.reflectv == Vector(0, math.sqrt(2) / 2, math.sqrt(2) / 2)


def check_n1_n2(index):
    a = GlassSphere()
    a.set_transform(Scaling(2, 2, 2))
    a.material.refractive_index = 1.5

    b = GlassSphere()
    b.set_transform(Translation(0, 0, -0.25))
    b.material.refractive_index = 2.0

    c = GlassSphere()
    c.set_transform(Translation(0, 0, 0.25))
    c.material.refractive_index = 2.5

    r = Ray(Point(0, 0, -4), Vector(0, 0, 1))
    xs = Intersections(
        Intersection(2, a),
        Intersection(2.75, b),
        Intersection(3.25, c),
        Intersection(4.75, b),
        Intersection(5.25, c),
        Intersection(6, a),
    )
    comps = xs[index].prepare_computation(r, xs)
    return (comps.n1, comps.n2)


def test_n_0():
    assert (1.0, 1.5) == check_n1_n2(0)


def test_n_1():
    assert (1.5, 2.0) == check_n1_n2(1)


def test_n_2():
    assert (2.0, 2.5) == check_n1_n2(2)


def test_n_3():
    assert (2.5, 2.5) == check_n1_n2(3)


def test_n_4():
    assert (2.5, 1.5) == check_n1_n2(4)


def test_n_5():
    assert (1.5, 1.0) == check_n1_n2(5)


def test_under_point():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = GlassSphere()
    s.set_transform(Translation(0, 0, 1))
    i = Intersection(5, s)
    xs = Intersections(i)
    comps = i.prepare_computation(r, xs)
    assert comps.under_point.z > EPSILON / 2
    assert comps.point.z < comps.under_point.z


def test_schlick_tir():
    rt2 = math.sqrt(2) / 2
    s = GlassSphere()
    r = Ray(Point(0, 0, rt2), Vector(0, 1, 0))
    xs = Intersections(Intersection(-rt2, s), Intersection(rt2, s))
    comps = xs[1].prepare_computation(r, xs)
    reflectance = comps.schlick()
    assert reflectance == 1.0


def test_schlick_perpendicular():
    s = GlassSphere()
    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    xs = Intersections(Intersection(-1, s), Intersection(1, s))
    comps = xs[1].prepare_computation(r, xs)
    reflectance = comps.schlick()
    assert equal(reflectance, 0.04)


def test_schlick_small_angle():
    s = GlassSphere()
    r = Ray(Point(0, 0.99, -2), Vector(0, 0, 1))
    xs = Intersections(Intersection(1.8589, s))
    comps = xs[0].prepare_computation(r, xs)
    reflectance = comps.schlick()
    assert equal(reflectance, 0.48873)
