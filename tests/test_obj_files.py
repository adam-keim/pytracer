from raytracer.parser import Parser
from raytracer.base import Point
import os

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_dir = os.path.join(current_directory, "obj_files")


def open_obj(name: str):
    return open(os.path.join(path_to_dir, name), "r")


def test_gibberish():
    f = open_obj("gibberish.obj")
    p = Parser(f)
    assert p.ignored == 5


def test_vertex():
    f = open_obj("vertex.obj")
    p = Parser(f)
    assert p.vertices[1] == Point(-1, 1, 0)
    assert p.vertices[2] == Point(-1, 0.5, 0)
    assert p.vertices[3] == Point(1, 0, 0)
    assert p.vertices[4] == Point(1, 1, 0)


def test_faces():
    f = open_obj("face.obj")
    p = Parser(f)
    g = p.default_group
    t1 = g.objects[0]
    t2 = g.objects[1]
    assert t1.p1 == p.vertices[1]
    assert t1.p2 == p.vertices[2]
    assert t1.p3 == p.vertices[3]
    assert t2.p1 == p.vertices[1]
    assert t2.p2 == p.vertices[3]
    assert t2.p3 == p.vertices[4]


def test_polygon():
    f = open_obj("polygon.obj")
    p = Parser(f)
    g = p.default_group
    t1 = g.objects[0]
    t2 = g.objects[1]
    t3 = g.objects[2]
    assert t1.p1 == p.vertices[1]
    assert t1.p2 == p.vertices[2]
    assert t1.p3 == p.vertices[3]
    assert t2.p1 == p.vertices[1]
    assert t2.p2 == p.vertices[3]
    assert t2.p3 == p.vertices[4]
    assert t3.p1 == p.vertices[1]
    assert t3.p2 == p.vertices[4]
    assert t3.p3 == p.vertices[5]


def test_groups():
    f = open_obj("groups.obj")
    p = Parser(f)
    g1 = p.get_named_group("FirstGroup")
    g2 = p.get_named_group("SecondGroup")
    t1 = g1.objects[0]
    t2 = g2.objects[0]
    assert t1.p1 == p.vertices[1]
    assert t1.p2 == p.vertices[2]
    assert t1.p3 == p.vertices[3]
    assert t2.p1 == p.vertices[1]
    assert t2.p2 == p.vertices[3]
    assert t2.p3 == p.vertices[4]


def test_obj_to_group():
    f = open_obj("groups.obj")
    p = Parser(f)
    g = p.obj_to_group()
    g1 = p.get_named_group("FirstGroup")
    g2 = p.get_named_group("SecondGroup")
    assert g1 in g.objects
    assert g2 in g.objects
