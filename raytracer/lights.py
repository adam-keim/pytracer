from raytracer.base import Point, Color


class PointLight:
    def __init__(self, pos: Point, intensity: Color):
        self.position = pos
        self.intensity = intensity

    def __eq__(self, other):
        return self.position == other.position and self.intensity == other.intensity
