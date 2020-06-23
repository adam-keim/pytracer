from raytracer.shapes import Group, _TestShape, Sphere
from raytracer.base import Identity, Point, Vector, Translation, Scaling
from raytracer.rays import Ray


def test_group_creation():
    g = Group()
    assert g.transform == Identity()
    assert len(g.objects) == 0


def test_add_child():
    g = Group()
    s = _TestShape()
    g.add_child(s)
    assert len(g.objects) > 0
    assert s.parent == g


def test_empty_group():
    g = Group()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = g.local_intersect(r)
    assert len(xs) == 0


def test_nonempty_group():
    g = Group()
    s1 = Sphere()
    s2 = Sphere()
    s2.set_transform(Translation(0, 0, -3))
    s3 = Sphere()
    s3.set_transform(Translation(5, 0, 0))
    g.add_child(s1)
    g.add_child(s2)
    g.add_child(s3)
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = g.local_intersect(r)
    assert len(xs) == 4
    assert xs[0].object == s2
    assert xs[1].object == s2
    assert xs[2].object == s1
    assert xs[3].object == s1


def test_transformed_group():
    g = Group()
    g.set_transform(Scaling(2, 2, 2))
    s = Sphere()
    s.set_transform(Translation(5, 0, 0))
    g.add_child(s)
    r = Ray(Point(10, 0, -10), Vector(0, 0, 1))
    xs = g.intersect(r)
    assert len(xs) == 2
