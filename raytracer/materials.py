from raytracer.base import Color, Point, Vector
from raytracer.lights import PointLight
from raytracer.patterns import StripePattern
import math


class Material:
    def __init__(
        self,
        color: Color = Color(1, 1, 1),
        ambient: float = 0.1,
        diffuse: float = 0.9,
        specular: float = 0.9,
        shininess: float = 200,
        reflective: float = 0.0,
        pattern: StripePattern = None,
        transparency: float = 0.0,
        index: float = 1.0,
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.pattern = pattern
        self.reflective = reflective
        self.transparency = transparency
        self.refractive_index = index

    def __eq__(self, other):
        return (
            self.color == other.color
            and self.ambient == other.ambient
            and self.diffuse == other.diffuse
            and self.specular == other.specular
            and self.shininess == other.shininess
            and self.pattern == other.pattern
            and self.reflective == other.reflective
            and self.transparency == other.transparency
            and self.refractive_index == other.refractive_index
        )

    def __str__(self):
        return f"{self.color}\nAmbient: {self.ambient}\nDiffuse: {self.diffuse}\nSpecular: {self.specular} \nShininess: {self.shininess}\n"

    def lighting(
        self,
        object,
        light: PointLight,
        position: Point,
        eyev: Vector,
        normalv: Vector,
        in_shadow: bool = False,
    ) -> Color:
        diffuse = Color(0, 0, 0)
        specular = Color(0, 0, 0)
        if self.pattern is not None:
            color = self.pattern.pattern_at_shape(object, position)
        else:
            color = self.color
        effective_color = color * light.intensity
        lightv = (light.position - position).normalize()
        ambient = effective_color * self.ambient
        if in_shadow:
            return ambient
        light_dot_normal = lightv.dot(normalv)
        if light_dot_normal >= 0:
            diffuse = effective_color * self.diffuse * light_dot_normal
            reflectv = -lightv.reflect(normalv)
            reflect_dot_eye = reflectv.dot(eyev)
            if reflect_dot_eye > 0:
                factor = math.pow(reflect_dot_eye, self.shininess)
                specular = light.intensity * self.specular * factor
        return ambient + diffuse + specular
