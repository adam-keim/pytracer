from raytracer.materials import Material
from raytracer.base import Color, Vector, Point
from raytracer.lights import PointLight
from raytracer.shapes import Sphere
from raytracer.patterns import StripePattern
import math


def test_default_material():
    m = Material()
    assert m.color == Color(1, 1, 1)
    assert m.ambient == 0.1
    assert m.diffuse == 0.9
    assert m.specular == 0.9
    assert m.shininess == 200


def test_lighting_eye_between():  # eye between light and surface
    s = Sphere()
    m = Material()
    p = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    res = m.lighting(s, light, p, eyev, normalv)
    assert res == Color(1.9, 1.9, 1.9)


def test_lighting_eye_offset():  # eye between light and surface, 45 offset
    s = Sphere()
    m = Material()
    p = Point(0, 0, 0)
    eyev = Vector(0, math.sqrt(2) / 2, -math.sqrt(2) / 2)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    res = m.lighting(s, light, p, eyev, normalv)
    assert res == Color(1.0, 1.0, 1.0)


def test_lighting_eye_opposite():  # eye opposite surface, 45 offset
    s = Sphere()
    m = Material()
    p = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    res = m.lighting(s, light, p, eyev, normalv)
    assert res == Color(0.7364, 0.7364, 0.7364)


def test_lighting_eye_in_path():  # eye in reflection path
    s = Sphere()
    m = Material()
    p = Point(0, 0, 0)
    eyev = Vector(0, -math.sqrt(2) / 2, -math.sqrt(2) / 2)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
    res = m.lighting(s, light, p, eyev, normalv)
    assert res == Color(1.6364, 1.6364, 1.6364)


def test_lighting_behind_surface():  # eye behind surface
    s = Sphere()
    m = Material()
    p = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Color(1, 1, 1))
    res = m.lighting(s, light, p, eyev, normalv)
    assert res == Color(0.1, 0.1, 0.1)


def test_surface_shadow():
    s = Sphere()
    m = Material()
    p = Point(0, 0, 0)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    in_shadow = True
    result = m.lighting(s, light, p, eyev, normalv, in_shadow)
    assert result == Color(0.1, 0.1, 0.1)


def test_lighting_pattern():
    s = Sphere()
    m = Material()
    m.pattern = StripePattern(Color(1, 1, 1), Color(0, 0, 0))
    m.ambient = 1
    m.diffuse = 0
    m.specular = 0
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    c1 = m.lighting(s, light, Point(0.9, 0, 0), eyev, normalv, False)
    c2 = m.lighting(s, light, Point(1.1, 0, 0), eyev, normalv, False)
    assert c1 == Color(1, 1, 1)
    assert c2 == Color(0, 0, 0)


def test_reflective_attribute():
    m = Material()
    assert m.reflective == 0.0


def test_transparency_and_index():
    m = Material()
    assert m.transparency == 0.0
    assert m.refractive_index == 1.0
