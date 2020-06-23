from raytracer.base import Point
from raytracer.shapes import Group, Triangle


class Parser:
    def __init__(self, file):
        self.ignored = 0
        self.vertices = [Point(0, 0, 0)]  # Add a point to start actual vertices at 1
        self.named_groups = {}
        self.default_group = Group()
        self.current_group = self.default_group
        for line in file:
            if line[0] == "v":
                point_values = line.split(" ")
                p = Point(
                    float(point_values[1]),
                    float(point_values[2]),
                    float(point_values[3]),
                )
                self.vertices.append(p)
            elif line[0] == "f":
                point_i = line.split(" ")
                print(list(map(lambda x: int(x), point_i[1:])))
                ts = self.fan_triangulation(list(map(lambda x: int(x), point_i[1:])))
                for t in ts:
                    self.current_group.add_child(t)
            elif line[0] == "g":
                group_name = line.split(" ")[1].strip()
                if self.get_named_group(group_name) is None:
                    self.create_named_group(group_name)
                self.current_group = self.named_groups[group_name]
                print(self.named_groups)

            else:
                self.ignored += 1

    def fan_triangulation(self, vertices_i):  # Takes indices of vertices
        ts = []
        for i in range(2, len(vertices_i)):
            tri = Triangle(
                self.vertices[vertices_i[0]],
                self.vertices[vertices_i[i - 1]],
                self.vertices[vertices_i[i]],
            )
            ts.append(tri)
        return ts

    def obj_to_group(self):
        g = Group()
        g.objects.append(self.default_group)
        for group in self.named_groups:
            g.objects.append(group)
        return g

    def get_named_group(self, group_name):
        return self.named_groups.get(group_name)

    def create_named_group(self, group_name):
        self.named_groups[group_name] = Group()
