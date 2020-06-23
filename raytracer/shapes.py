from raytracer.rays import Ray, Intersections, Intersection
from raytracer.base import Point, Identity, Matrix, Vector, EPSILON
from raytracer.materials import Material
import math


class Shape:
    def __init__(self):
        self.transform = Identity()
        self.material = Material()
        self.parent = None

    def set_material(self, material: Material):
        self.material = material

    def set_transform(self, t: Matrix):
        self.transform *= t

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.material == other.material
            and self.parent == other.parent
            and self.transform == other.transform
        )

    def intersect(self, ray: Ray):
        local_ray = ray.transform(self.transform.inverse())
        return self.local_intersect(local_ray)

    def normal_at(self, world_point: Point):
        local_point = self.world_to_object(world_point)
        local_normal = self.local_normal_at(local_point)
        return self.normal_to_world(local_normal)

    def world_to_object(self, point: Point):
        if self.parent is not None:
            point = self.parent.world_to_object(point)
        return self.transform.inverse() * point

    def normal_to_world(self, normal: Vector):
        normalv = self.transform.inverse().transpose() * normal
        normalv.w = 0
        normalv = normalv.normalize()

        if self.parent is not None:
            normalv = self.parent.normal_to_world(normalv)

        return normalv

    def local_normal_at(self, local_point):
        raise TypeError("Generic Shapes cannot be evaluated")

    def local_intersect(self, ray):
        raise TypeError("Generic Shapes cannot be evaluated")

    def __str__(self):
        return f"{self.__class__}: Transform:\n{self.transform}"


class _TestShape(Shape):
    def __init__(self):
        super().__init__()

    def local_intersect(self, ray: Ray):
        self.saved_ray = ray

    def local_normal_at(self, point):
        return Vector(point.x, point.y, point.z)


class Sphere(Shape):
    def __init__(self):
        self.origin = Point(0, 0, 0)
        self.radius = 1
        super().__init__()

    def local_intersect(self, ray: Ray):
        obj_to_ray = ray.origin - self.origin
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(obj_to_ray)
        c = obj_to_ray.dot(obj_to_ray) - 1

        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return Intersections()

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return Intersections(Intersection(t1, self), Intersection(t2, self))

    def local_normal_at(self, point: Point):
        return point - self.origin

    def __eq__(self, other):
        return (
            isinstance(other, Sphere)
            and self.origin == other.origin
            and self.radius == other.radius
            and self.transform == other.transform
            and self.material == other.material
        )


class GlassSphere(Sphere):
    def __init__(self):
        super().__init__()
        self.material.transparency = 1.0
        self.material.refractive_index = 1.5


class Plane(Shape):
    def __init__(self):
        super().__init__()

    def local_normal_at(self, point: Point):
        return Vector(0, 1, 0)

    def local_intersect(self, ray: Ray):
        if abs(ray.direction.y) < EPSILON:
            return Intersections()
        t = -ray.origin.y / ray.direction.y
        return Intersections(Intersection(t, self))


# CUBE CHECK AXIS HELPER FUNCTION
def check_axis(origin, direction) -> (float, float):
    tmin_numerator = -1 - origin
    tmax_numerator = 1 - origin
    if abs(direction) >= EPSILON:
        tmin = tmin_numerator / direction
        tmax = tmax_numerator / direction
    else:
        tmin = tmin_numerator * math.inf
        tmax = tmax_numerator * math.inf
    if tmin > tmax:
        tmin, tmax = (tmax, tmin)
    return (tmin, tmax)


class Cube(Shape):
    def __init__(self):
        super().__init__()

    def local_intersect(self, ray: Ray):
        xtmin, xtmax = check_axis(ray.origin.x, ray.direction.x)
        ytmin, ytmax = check_axis(ray.origin.y, ray.direction.y)
        ztmin, ztmax = check_axis(ray.origin.z, ray.direction.z)
        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)
        if tmin > tmax:
            return Intersections()
        else:
            return Intersections(Intersection(tmin, self), Intersection(tmax, self))

    def local_normal_at(self, point: Point):
        maxc = max(abs(point.x), abs(point.y), abs(point.z))
        if maxc == abs(point.x):
            return Vector(point.x, 0, 0)
        elif maxc == abs(point.y):
            return Vector(0, point.y, 0)
        else:
            return Vector(0, 0, point.z)


def check_cap(ray: Ray, t: float, radius: float) -> bool:
    x = ray.origin.x + t * ray.direction.x
    z = ray.origin.z + t * ray.direction.z
    return (x ** 2 + z ** 2) <= abs(radius)


class Cylinder(Shape):
    def __init__(self):
        self.minimum = -math.inf
        self.maximum = math.inf
        self.closed = False
        super().__init__()

    def local_intersect(self, ray: Ray):
        a = ray.direction.x ** 2 + ray.direction.z ** 2
        if abs(a) < EPSILON:
            xs = Intersections()
            self.intersect_caps(ray, xs)
            return xs

        b = 2 * ray.origin.x * ray.direction.x + 2 * ray.origin.z * ray.direction.z
        c = ray.origin.x ** 2 + ray.origin.z ** 2 - 1
        disc = b ** 2 - 4 * a * c
        if disc < 0:
            return Intersections()

        t0 = (-b - math.sqrt(disc)) / (2 * a)
        t1 = (-b + math.sqrt(disc)) / (2 * a)

        if t0 > t1:
            t0, t1 = (t1, t0)

        xs = Intersections()

        y0 = ray.origin.y + t0 * ray.direction.y
        if self.minimum < y0 and y0 < self.maximum:
            xs.append(Intersection(t0, self))

        y1 = ray.origin.y + t1 * ray.direction.y
        if self.minimum < y1 and y1 < self.maximum:
            xs.append(Intersection(t1, self))

        self.intersect_caps(ray, xs)
        return xs

    def local_normal_at(self, point: Point):
        dist = point.x ** 2 + point.z ** 2
        if dist < 1 and point.y >= self.maximum - EPSILON:
            return Vector(0, 1, 0)
        elif dist < 1 and point.y <= self.minimum + EPSILON:
            return Vector(0, -1, 0)
        else:
            return Vector(point.x, 0, point.z)

    def intersect_caps(self, ray: Ray, xs):
        if self.closed == False or abs(ray.direction.y) < EPSILON:
            return

        t_lower = (self.minimum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t_lower, 1):
            xs.append(Intersection(t_lower, self))

        t_upper = (self.maximum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t_upper, 1):
            xs.append(Intersection(t_upper, self))


class Cone(Shape):
    def __init__(self):
        self.minimum = -math.inf
        self.maximum = math.inf
        self.closed = False
        super().__init__()

    def local_intersect(self, ray: Ray):
        a = ray.direction.x ** 2 - ray.direction.y ** 2 + ray.direction.z ** 2
        b = (
            2 * ray.origin.x * ray.direction.x
            - 2 * ray.origin.y * ray.direction.y
            + 2 * ray.origin.z * ray.direction.z
        )
        c = ray.origin.x ** 2 - ray.origin.y ** 2 + ray.origin.z ** 2

        if abs(a) < EPSILON:
            xs = Intersections()
            if abs(b) > EPSILON:
                t = -c / (2 * b)
                xs.append(Intersection(t, self))
            self.intersect_caps(ray, xs)
            return xs

        disc = b ** 2 - 4 * a * c
        if disc < 0:
            return Intersections()

        t0 = (-b - math.sqrt(disc)) / (2 * a)
        t1 = (-b + math.sqrt(disc)) / (2 * a)

        if t0 > t1:
            t0, t1 = (t1, t0)

        xs = Intersections()

        y0 = ray.origin.y + t0 * ray.direction.y
        if self.minimum < y0 and y0 < self.maximum:
            xs.append(Intersection(t0, self))

        y1 = ray.origin.y + t1 * ray.direction.y
        if self.minimum < y1 and y1 < self.maximum:
            xs.append(Intersection(t1, self))

        self.intersect_caps(ray, xs)
        return xs

    def intersect_caps(self, ray: Ray, xs):
        if self.closed == False or abs(ray.direction.y) < EPSILON:
            return

        t_lower = (self.minimum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t_lower, self.minimum):
            xs.append(Intersection(t_lower, self))

        t_upper = (self.maximum - ray.origin.y) / ray.direction.y
        if check_cap(ray, t_upper, self.maximum):
            xs.append(Intersection(t_upper, self))

    def local_normal_at(self, point: Point):
        dist = point.x ** 2 + point.z ** 2
        y = math.sqrt(dist)
        if point.y > 0:
            y = -y
        if dist < 1 and point.y >= self.maximum - EPSILON:
            return Vector(0, 1, 0)
        elif dist < 1 and point.y <= self.minimum + EPSILON:
            return Vector(0, -1, 0)
        else:
            return Vector(point.x, y, point.z)


class Group(Shape):
    def __init__(self):
        self.objects = []
        super().__init__()

    def add_child(self, object):
        self.objects.append(object)
        object.parent = self

    def local_intersect(self, ray: Ray):
        total_xs = Intersections()
        for obj in self.objects:
            xs = obj.intersect(ray)
            total_xs.extend(xs)
        total_xs.sort()
        for x in total_xs:
            print(x)
        return total_xs


class Triangle(Shape):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.e1 = p2 - p1
        self.e2 = p3 - p1
        self.normal = self.e2.cross(self.e1).normalize()
        super().__init__()

    def local_normal_at(self, point: Point):
        return self.normal

    def local_intersect(self, ray: Ray):
        dir_cross_e2 = ray.direction.cross(self.e2)
        det = self.e1.dot(dir_cross_e2)
        if abs(det) < EPSILON:
            return Intersections()

        f = 1.0 / det
        p1_to_origin = ray.origin - self.p1
        u = f * p1_to_origin.dot(dir_cross_e2)
        if u < 0 or u > 1:
            return Intersections()

        origin_cross_e1 = p1_to_origin.cross(self.e1)
        v = f * ray.direction.dot(origin_cross_e1)
        if v < 0 or (u + v) > 1:
            return Intersections()

        t = f * self.e2.dot(origin_cross_e1)
        return Intersections(Intersection(t, self))  # BOGUS TO TEST AGAINST POSITIVE

    def __str__(self):
        return f"Triangle: p1: {self.p1}, p2: {self.p2}, p3: {self.p3}"
