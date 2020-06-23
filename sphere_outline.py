from raytracer import base, rays, shapes, materials, lights, patterns

CANVAS_PIXELS = 256
COLOR = base.Color(1, 0, 0)


shape = shapes.Sphere()
shape.material = materials.Material()
shape.material.color = base.Color(0.1, 1, 0)
shape.material.pattern = patterns.StripePattern(
    base.Color(1, 1, 1), base.Color(0, 0, 0)
)

light_position = base.Point(-10, 10, -10)
light_color = base.Color(1, 1, 1)
light = lights.PointLight(light_position, light_color)

ray_origin = base.Point(0, 0, -5)
wall_z = 10
wall_size = 7

pixel_size = wall_size / CANVAS_PIXELS
half = wall_size / 2

c = base.Canvas(CANVAS_PIXELS, CANVAS_PIXELS)
for y in range(CANVAS_PIXELS):
    print(y)
    world_y = half - pixel_size * y
    for x in range(CANVAS_PIXELS):
        world_x = -half + pixel_size * x

        position = base.Point(world_x, world_y, wall_z)

        r = rays.Ray(ray_origin, (position - ray_origin).normalize())
        xs = shape.intersect(r)
        if xs.hit() is not None:
            point = r.position(xs.hit().t)
            normal = xs.hit().object.normal_at(point)
            eye = -r.direction
            color = shape.material.lighting(shape, light, point, eye, normal)
            c.write_pixel(x, y, color)


with open("sphere.ppm", "w") as f:
    f.write(c.to_ppm())
