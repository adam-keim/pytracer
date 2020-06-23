from raytracer.base import Identity, Canvas, Matrix, Point
from raytracer.world import World
from raytracer.rays import Ray

import math


class Camera:
    def __init__(self, hsize: int, vsize: int, fov: float, transform: Matrix = None):
        self.hsize = hsize
        self.vsize = vsize
        self.fov = fov
        if transform is None:
            self.transform = Identity()
        else:
            self.transform = transform

        half_view = math.tan(self.fov / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view
        self.pixel_size = (self.half_width * 2) / self.hsize

    def ray_for_pixel(self, px, py):
        x_offset = (px + 0.5) * self.pixel_size
        y_offset = (py + 0.5) * self.pixel_size

        world_x = self.half_width - x_offset
        world_y = self.half_height - y_offset

        pixel = self.transform.inverse() * Point(world_x, world_y, -1)
        origin = self.transform.inverse() * Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        return Ray(origin, direction)

    def render(self, world: World):
        image = Canvas(self.hsize, self.vsize)
        for y in range(self.vsize):
            print(y)
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                image.write_pixel(x, y, color)
        return image
