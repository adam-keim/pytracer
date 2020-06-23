from raytracer.shapes import Sphere, Shape, GlassSphere
from raytracer.base import Vector, Point, Identity, Translation, Scaling, RotationZ
from raytracer.rays import Ray
from raytracer.materials import Material
import math


def test_ray_sphere_intersect():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    i = s.intersect(r)
    assert len(i) == 2
    assert i[0].t == 4.0
    assert i[1].t == 6.0


def test_ray_tangent_intersect():
    r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
    s = Sphere()
    i = s.intersect(r)
    assert len(i) == 2
    assert i[0].t == 5.0
    assert i[1].t == 5.0


def test_ray_miss():
    r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
    s = Sphere()
    i = s.intersect(r)
    assert len(i) == 0


def test_ray_in_sphere():
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    s = Sphere()
    i = s.intersect(r)
    assert len(i) == 2
    assert i[0].t == -1
    assert i[1].t == 1


def test_sphere_behind_ray():
    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    s = Sphere()
    i = s.intersect(r)
    assert len(i) == 2
    assert i[0].t == -6.0
    assert i[1].t == -4.0


def test_object_intersect():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].object == s
    assert xs[1].object == s


def test_sphere_x_normal():
    s = Sphere()
    n = s.normal_at(Point(1, 0, 0))
    assert n == Vector(1, 0, 0)


def test_sphere_y_normal():
    s = Sphere()
    n = s.normal_at(Point(1, 0, 0))
    assert n == Vector(1, 0, 0)


def test_sphere_z_normal():
    s = Sphere()
    n = s.normal_at(Point(0, 0, 1))
    assert n == Vector(0, 0, 1)


def test_sphere_nonaxial_normal():
    s = Sphere()
    num = math.sqrt(3) / 3
    n = s.normal_at(Point(num, num, num))
    assert n == Vector(num, num, num)


def test_normal_is_normal():
    s = Sphere()
    num = math.sqrt(3) / 3
    n = s.normal_at(Point(num, num, num))
    assert n == n.normalize()


def test_sphere_is_shape():
    s = Sphere()
    assert isinstance(s, Shape)


def test_glassy_sphere():
    s = GlassSphere()
    assert s.transform == Identity()
    assert s.material.transparency == 1.0
    assert s.material.refractive_index == 1.5
