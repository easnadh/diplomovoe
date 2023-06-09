from dataclasses import dataclass

from mesh.point3d import Point3D


@dataclass(slots=True)
class Edge3D:
    first: Point3D
    second: Point3D

    def __repr__(self):
        return f'Edge3D({", ".join(map(repr, self.points))})'

    @property
    def points(self):
        return self.first, self.second
