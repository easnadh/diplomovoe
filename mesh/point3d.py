from dataclasses import dataclass


@dataclass(slots=True)
class Point3D:
    x: float
    y: float
    z: float

    def __repr__(self):
        return f'Point3D({self.x}, {self.y}, {self.z})'

    def __hash__(self):
        return hash(self.__repr__())

    def __copy__(self):
        return Point3D(self.x, self.y, self.z)
