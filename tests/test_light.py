from raytracer.base import Point, Color
from raytracer.lights import PointLight
import math


def test_light_attributes():
    position = Point(0, 0, 0)
    intensity = Color(1, 1, 1)
    light = PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity
