from raytracer.shapes import Shape, _TestShape, Group, Sphere
from raytracer.base import (
    Identity,
    Translation,
    Scaling,
    Point,
    Vector,
    RotationZ,
    RotationY,
)
from raytracer.materials import Material
from raytracer.rays import Ray
import math


def test_default_transform():
    s = _TestShape()
    assert s.transform == Identity()


def test_assign_transform():
    s = _TestShape()
    s.set_transform(Translation(2, 3, 4))
    assert s.transform == Translation(2, 3, 4)


def test_default_material():
    s = _TestShape()
    assert s.material == Material()


def test_assign_material():
    s = _TestShape()
    m = Material()
    m.ambient = 1
    s.set_material(m)
    assert s.material == m


def test_scaled_shape_intersection():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = _TestShape()
    s.set_transform(Scaling(2, 2, 2))
    _ = s.intersect(r)
    assert s.saved_ray.origin == Point(0, 0, -2.5)
    assert s.saved_ray.direction == Vector(0, 0, 0.5)


def test_translated_shape_intersection():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = _TestShape()
    s.set_transform(Translation(5, 0, 0))
    _ = s.intersect(r)
    assert s.saved_ray.origin == Point(-5, 0, -5)
    assert s.saved_ray.direction == Vector(0, 0, 1)


def test_translated_shape_normal():
    s = _TestShape()
    s.set_transform(Translation(0, 1, 0))
    n = s.normal_at(Point(0, 1.70711, -0.70711))
    assert n == Vector(0, 0.70711, -0.70711)


def test_transformed_shape_normal():
    s = _TestShape()
    t = Scaling(1, 0.5, 1) * RotationZ(math.pi / 5)
    s.set_transform(t)
    n = s.normal_at(Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2))
    assert n == Vector(0, 0.97014, -0.24254)


def test_shape_has_parent():
    s = _TestShape()
    assert s.parent is None


def test_world_to_object():
    g1 = Group()
    g1.set_transform(RotationY(math.pi / 2))
    g2 = Group()
    g2.set_transform(Scaling(2, 2, 2))
    g1.add_child(g2)
    s = Sphere()
    s.set_transform(Translation(5, 0, 0))
    g2.add_child(s)
    p = s.world_to_object(Point(-2, 0, -10))
    assert p == Point(0, 0, -1)


def test_normal_object_to_world():
    g1 = Group()
    g1.set_transform(RotationY(math.pi / 2))
    g2 = Group()
    g2.set_transform(Scaling(1, 2, 3))
    g1.add_child(g2)
    s = Sphere()
    s.set_transform(Translation(5, 0, 0))
    g2.add_child(s)
    n = s.normal_to_world(Vector(math.sqrt(3) / 3, math.sqrt(3) / 3, math.sqrt(3) / 3))
    assert n == Vector(0.2857, 0.4286, -0.8571)


def test_child_normal():
    g1 = Group()
    g1.set_transform(RotationY(math.pi / 2))
    g2 = Group()
    g2.set_transform(Scaling(1, 2, 3))
    g1.add_child(g2)
    s = Sphere()
    s.set_transform(Translation(5, 0, 0))
    g2.add_child(s)
    n = s.normal_at(Point(1.7321, 1.1547, -5.5774))
    assert n == Vector(0.2857, 0.4286, -0.8571)
