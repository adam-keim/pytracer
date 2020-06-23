from raytracer.world import World
from raytracer.base import Point, Vector, Color, Scaling, Translation, EPSILON
from raytracer.materials import Material
from raytracer.rays import Ray, Intersection, Intersections
from raytracer.shapes import Sphere, Plane
from raytracer.lights import PointLight
from raytracer.patterns import _TestPattern
import math


def test_empty_world():
    w = World()
    assert len(w.objects) == 0
    assert w.light is None


def test_default_world():
    light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
    s1 = Sphere()
    m = Material()
    m.color = Color(0.8, 1.0, 0.6)
    m.diffuse = 0.7
    m.specular = 0.2
    s1.set_material(m)
    s2 = Sphere()
    t = Scaling(0.5, 0.5, 0.5)
    s2.set_transform(t)
    w = World.default()
    assert w.light == light
    assert s1 in w.objects
    assert s2 in w.objects


def test_ray_world():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = w.intersect(r)
    assert len(xs) == 4
    assert xs[0].t == 4
    assert xs[1].t == 4.5
    assert xs[2].t == 5.5
    assert xs[3].t == 6


def test_intersection_shading():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = w.objects[0]
    i = Intersection(4, shape)
    comps = i.prepare_computation(r)
    c = w.shade_hit(comps)
    assert c == Color(0.38066, 0.47583, 0.2855)


def test_inside_intersection_shading():
    w = World.default()
    w.light = PointLight(Point(0, 0.25, 0), Color(1, 1, 1))
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w.objects[1]
    i = Intersection(0.5, shape)
    comps = i.prepare_computation(r)
    c = w.shade_hit(comps)
    assert c == Color(0.90498, 0.90498, 0.90498)


def test_ray_miss():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    c = w.color_at(r)
    assert c == Color(0, 0, 0)


def test_ray_hit():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    c = w.color_at(r)
    assert c == Color(0.38066, 0.47583, 0.2855)


def test_intersection_behind_ray():
    w = World.default()
    outer = w.objects[0]
    outer.material.ambient = 1
    inner = w.objects[1]
    inner.material.ambient = 1
    r = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
    c = w.color_at(r)
    assert c == inner.material.color


def test_no_colinear_shadow():
    w = World.default()
    p = Point(0, 10, 0)
    assert not w.is_shadowed(p)


def test_shadow_occlusion():
    w = World.default()
    p = Point(10, -10, 10)
    assert w.is_shadowed(p)


def test_no_shadow_behind_light():
    w = World.default()
    p = Point(-20, 20, -20)
    assert not w.is_shadowed(p)


def test_no_shadow_behind_point():
    w = World.default()
    p = Point(-2, 2, -2)
    assert not w.is_shadowed(p)


def test_shadow_shade_hit():
    w = World()
    w.light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    s1 = Sphere()
    s2 = Sphere()
    s2.set_transform(Translation(0, 0, 10))
    w.objects.extend([s1, s2])
    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    i = Intersection(4, s2)
    comps = i.prepare_computation(r)
    c = w.shade_hit(comps)
    print(c)
    assert c == Color(0.1, 0.1, 0.1)


def test_hit_offset():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    shape.set_transform(Translation(0, 0, 1))
    i = Intersection(5, shape)
    comps = i.prepare_computation(r)
    assert comps.over_point.z < -EPSILON / 2
    assert comps.point.z > comps.over_point.z


def test_reflected_color_nonreflective():
    w = World().default()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    s = w.objects[0]
    s.material.ambient = 1
    i = Intersection(1, s)
    comps = i.prepare_computation(r)
    c = w.reflected_color(comps)
    assert c == Color(0, 0, 0)


def test_reflected_color():
    w = World().default()
    s = Plane()
    s.material.reflective = 0.5
    s.set_transform(Translation(0, -1, 0))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), s)
    comps = i.prepare_computation(r)
    c = w.reflected_color(comps)
    print(c)
    assert c == Color(0.19032, 0.2379, 0.14274)


def test_shade_hit_reflective():
    w = World().default()
    s = Plane()
    s.material.reflective = 0.5
    s.set_transform(Translation(0, -1, 0))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), s)
    comps = i.prepare_computation(r)
    c = w.shade_hit(comps)
    assert c == Color(0.87677, 0.92436, 0.82918)


def test_mutually_reflective_color_at():
    w = World()
    w.light = PointLight(Point(0, 0, 0), Color(1, 1, 1))
    lower = Plane()
    lower.material.reflective = 1
    lower.set_transform(Translation(0, -1, 0))
    w.objects.append(lower)
    upper = Plane()
    upper.material.reflective = 1
    upper.set_transform(Translation(0, 1, 0))
    w.objects.append(upper)
    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    assert w.color_at(r) is not None


def test_maximum_recursion_depth_color_at():
    w = World().default()
    s = Plane()
    s.material.reflective = 0.5
    s.set_transform(Translation(0, -1, 0))
    w.objects.append(s)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), s)
    comps = i.prepare_computation(r)
    color = w.reflected_color(comps, 0)
    assert color == Color(0, 0, 0)


def test_refracted_opaque():
    w = World().default()
    s = w.objects[0]
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(Intersection(4, s), Intersection(6, s))
    comps = xs[0].prepare_computation(r, xs)
    c = w.refracted_color(comps, 5)
    assert c == Color(0, 0, 0)


def test_refracted_max_depth():
    w = World().default()
    s = w.objects[0]
    s.material.transparency = 1.0
    s.material.refractive_index = 1.5
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(Intersection(4, s), Intersection(6, s))
    comps = xs[0].prepare_computation(r, xs)
    c = w.refracted_color(comps, 0)
    assert c == Color(0, 0, 0)


def test_refracted_total():
    w = World().default()
    s = w.objects[0]
    s.material.transparency = 1.0
    s.material.refractive_index = 1.5
    r = Ray(Point(0, 0, math.sqrt(2) / 2), Vector(0, 1, 0))
    xs = Intersections(
        Intersection(-math.sqrt(2) / 2, s), Intersection(math.sqrt(2) / 2, s)
    )
    comps = xs[1].prepare_computation(r, xs)
    c = w.refracted_color(comps, 5)
    assert c == Color(0, 0, 0)


def test_refracted_color():
    w = World().default()
    a = w.objects[0]
    a.material.ambient = 1.0
    a.material.pattern = _TestPattern()
    b = w.objects[1]
    b.material.transparency = 1.0
    b.material.refractive_index = 1.5
    r = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
    xs = Intersections(
        Intersection(-0.9899, a),
        Intersection(-0.4899, b),
        Intersection(0.4899, b),
        Intersection(0.9899, a),
    )
    comps = xs[2].prepare_computation(r, xs)
    c = w.refracted_color(comps, 5)
    print(c)
    assert c == Color(0, 0.99888, 0.04725)


def shade_hit_transparent():
    w = World().default()
    floor = Plane()
    floor.set_transform(Translation(0, -1, 0))
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.objects.append(floor)
    ball = Sphere()
    ball.material.color = Color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.set_transform(Translation(0, -3.5, -0.5))
    w.objects.append(ball)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    xs = Intersections(Intersection(math.sqrt(2), floor))
    comps = xs[0].prepare_computations(r, xs)
    color = w.shade_hit(comps, 5)
    assert color == Color(0.93642, 0.68642, 0.68642)


def shade_hit_reflective_transparent():
    rt2o2 = math.sqrt(2) / 2
    w = World().default()
    r = Ray(Point(0, 0, -3), Vector(0, -rt2o2, rt2o2))
    floor = Plane()
    floor.set_transform(Translation(0, -1, 0))
    floor.material.reflective = 0.5
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.objects.append(floor)
    ball = Sphere()
    ball.material.color = Color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.set_transform(Translation(0, -3.5, -0.5))
    w.objects.append(ball)
    xs = Intersections(Intersection(rt2o2, floor))
    comps = xs[0].prepare_computations(r, xs)
    color = w.shade_hit(comps, 5)
    assert color == Color(0.93391, 0.69643, 0.69243)
