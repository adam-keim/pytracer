from raytracer.base import Point, Color, Identity, Matrix
import math


class Pattern:
    def __init__(self):
        self.transform = Identity()

    def set_pattern_transform(self, t: Matrix):
        self.transform *= t

    def pattern_at_shape(self, shape, world_point: Point):
        object_point = shape.world_to_object(world_point)
        pattern_point = self.transform.inverse() * object_point
        return self.pattern_at(pattern_point)

    def pattern_at(self, point):
        raise TypeError("Generic Pattern Cannot be evaluated")


class _TestPattern(Pattern):
    def __init__(self):
        super().__init__()

    def pattern_at(self, point: Point):
        return Color(point.x, point.y, point.z)


class StripePattern(Pattern):
    def __init__(self, a: Color, b: Color):
        super().__init__()
        self.a = a
        self.b = b

    def pattern_at(self, point: Point):
        if math.floor(point.x) % 2 == 0:
            return self.a
        else:
            return self.b


class GradientPattern(Pattern):
    def __init__(self, a: Color, b: Color):
        super().__init__()
        self.a = a
        self.b = b

    def pattern_at(self, point: Point):
        distance = self.b - self.a
        fraction = point.x - math.floor(point.x)
        return self.a + (distance * fraction)


class RingPattern(Pattern):
    def __init__(self, a: Color, b: Color):
        super().__init__()
        self.a = a
        self.b = b

    def pattern_at(self, point: Point):
        if math.floor(math.sqrt((point.x ** 2) + (point.z ** 2))) % 2 == 0:
            return self.a
        else:
            return self.b


class CheckersPattern(Pattern):
    def __init__(self, a: Color, b: Color):
        super().__init__()
        self.a = a
        self.b = b

    def pattern_at(self, point: Point):
        if (math.floor(point.x) + math.floor(point.y) + math.floor(point.z)) % 2 == 0:
            return self.a
        else:
            return self.b
