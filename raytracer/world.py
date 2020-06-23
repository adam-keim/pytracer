from raytracer.base import Point, Color, Scaling
from raytracer.shapes import Sphere
from raytracer.lights import PointLight
from raytracer.materials import Material
from raytracer.rays import Ray, Intersections

import math

MAXBOUNCE = 5


class World:
    def __init__(self):
        self.light = None
        self.objects = []

    @classmethod
    def default(cls):
        world = cls()
        world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
        m = Material()
        m.color = Color(0.8, 1.0, 0.6)
        m.diffuse = 0.7
        m.specular = 0.2
        s1 = Sphere()
        s1.set_material(m)
        s2 = Sphere()
        s2.set_transform(Scaling(0.5, 0.5, 0.5))
        world.objects.extend([s1, s2])
        return world

    def intersect(self, ray):
        xs = Intersections()
        for obj in self.objects:
            xs.extend(obj.intersect(ray))
        xs.sort()
        return xs

    def shade_hit(self, comps, remaining: int = MAXBOUNCE) -> Color:
        shadowed = self.is_shadowed(comps.over_point)
        surface = comps.object.material.lighting(
            comps.object,
            self.light,
            comps.over_point,
            comps.eyev,
            comps.normalv,
            shadowed,
        )
        reflected = self.reflected_color(comps, remaining)
        refracted = self.refracted_color(comps, remaining)

        material = comps.object.material
        if material.reflective > 0 and material.transparency > 0:
            reflectance = comps.schlick()
            return surface + reflected * reflectance + refracted * (1 - reflectance)
        else:
            return surface + reflected + refracted

    def color_at(self, ray: Ray, remaining: int = MAXBOUNCE) -> Color:
        xs = self.intersect(ray)
        hit = xs.hit()
        if hit is None:
            return Color(0, 0, 0)
        else:
            return self.shade_hit(hit.prepare_computation(ray, xs), remaining)

    def reflected_color(self, comps, remaining: int = MAXBOUNCE) -> Color:
        if remaining < 1:
            return Color(0, 0, 0)
        if comps.object.material.reflective == 0:
            return Color(0, 0, 0)
        reflect_ray = Ray(comps.over_point, comps.reflectv)
        color = self.color_at(reflect_ray, remaining - 1)
        return color * comps.object.material.reflective

    def refracted_color(self, comps, remaining: int = MAXBOUNCE) -> Color:
        if remaining < 1:
            return Color(0, 0, 0)
        if comps.object.material.transparency == 0:
            return Color(0, 0, 0)

        n_ratio = comps.n1 / comps.n2
        cos_i = comps.eyev.dot(comps.normalv)
        sin2_t = (n_ratio ** 2) * (1 - (cos_i ** 2))
        if sin2_t > 1:
            return Color(0, 0, 0)

        cos_t = math.sqrt(1.0 - sin2_t)
        direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio
        refract_ray = Ray(comps.under_point, direction)
        color = (
            self.color_at(refract_ray, remaining - 1)
            * comps.object.material.transparency
        )
        return color

    def is_shadowed(self, point: Point) -> bool:
        v = self.light.position - point
        distance = v.magnitude()
        direction = v.normalize()

        r = Ray(point, direction)
        xs = self.intersect(r)
        h = xs.hit()
        if h is not None and h.t < distance:
            return True
        else:
            return False
