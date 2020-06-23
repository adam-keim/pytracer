from raytracer.base import Point, Vector, Matrix, EPSILON
from typing import NamedTuple, Any
import math


class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def position(self, time: float):
        return self.origin + self.direction * time

    def transform(self, m: Matrix):
        return Ray(m * self.origin, m * self.direction)


class Intersection:
    def __init__(self, t: float, object: object):
        self.t = t
        self.object = object

    def __lt__(self, other):
        return self.t < other.t

    def __eq__(self, other):
        return self.t == other.t and self.object == other.object

    def prepare_computation(self, ray: Ray, xs=None):
        if xs is None:
            xs = Intersections(self)
        point = ray.position(self.t)
        eyev = -ray.direction
        normalv = self.object.normal_at(point)
        if normalv.dot(eyev) < 0:
            inside = True
            normalv = -normalv
        else:
            inside = False
        reflectv = ray.direction.reflect(normalv)
        over_point = point + (normalv * EPSILON)
        under_point = point - (normalv * EPSILON)

        containers = []
        for i in xs:
            if i == self:
                if len(containers) == 0:
                    n1 = 1.0
                else:
                    n1 = containers[-1].material.refractive_index

            if i.object in containers:
                containers.remove(i.object)
            else:
                containers.append(i.object)

            if i == self:
                if len(containers) == 0:
                    n2 = 1.0
                else:
                    n2 = containers[-1].material.refractive_index
                break

        return Comps(
            self.t,
            self.object,
            point,
            eyev,
            normalv,
            reflectv,
            inside,
            over_point,
            under_point,
            n1,
            n2,
        )

    def __str__(self):
        return f"Intersection [time: {self.t}, object: {self.object}]"


class Comps(NamedTuple):
    t: float
    object: Any
    point: Point
    eyev: Vector
    normalv: Vector
    reflectv: Vector
    inside: bool
    over_point: Point
    under_point: Point
    n1: float
    n2: float

    def schlick(self) -> float:
        cos = self.eyev.dot(self.normalv)
        if self.n1 > self.n2:
            n = self.n1 / self.n2
            sin2_t = n ** 2 * (1.0 - cos ** 2)
            if sin2_t > 1.0:
                return 1.0

            cos_t = math.sqrt(1.0 - sin2_t)
            cos = cos_t

        r0 = ((self.n1 - self.n2) / (self.n1 + self.n2)) ** 2
        return r0 + (1 - r0) * ((1 - cos) ** 5)


# function schlick(comps)
# # find the cosine of the angle between the eye and normal vectors
# cos ← dot(comps.eyev, comps.normalv)
# # total internal reflection can only occur if n1 > n2
# if comps.n1 > comps.n2
# n ← comps.n1 / comps.n2
# sin2_t = n^2 * (1.0 - cos^2)
# return 1.0 if sin2_t > 1.0
# ➤ # compute cosine of theta_t using trig identity
# ➤ cos_t ← sqrt(1.0 - sin2_t)
# ➤
# ➤ # when n1 > n2, use cos(theta_t) instead
# ➤ cos ← cos_t
# end if
# ➤ r0 ← ((comps.n1 - comps.n2) / (comps.n1 + comps.n2))^2
# ➤ return r0 + (1 - r0) * (1 - cos)^5
# end function


class Intersections(list):
    def __init__(self, *args):
        super(Intersections, self).__init__(args)

    def hit(self) -> Intersection:
        hit = None
        for i in self:
            if i.t > 0 and (hit is None or i.t < hit.t):
                hit = i
        return hit
