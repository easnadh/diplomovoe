from dataclasses import dataclass
from itertools import combinations

from mesh.edge3d import Edge3D
from mesh.point3d import Point3D


class Triangle3D:
    __slots__ = ('points',)
    points: list[Point3D]

    def __init__(self, *points: Point3D):
        self.points = list(points)

    def __repr__(self):
        return f'Triangle3D({", ".join(map(repr, self.points))})'

    @classmethod
    def from_edges(cls, *edges: Edge3D):
        points = set()
        for edge in edges:
            points |= set(edge.points)
        return cls(*points)

    @property
    def edges(self) -> list[Edge3D]:
        edges: list[Edge3D] = []
        for p1, p2 in combinations(self.points, 2):
            edges.append(Edge3D(p1, p2))
        return edges
