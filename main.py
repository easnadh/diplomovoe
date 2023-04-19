from mesh.tetmesh import TetMesh
from utils.mesh_composition import mesh_composition


def main():
    tetmesh1 = TetMesh.read_from_file('cube.vol')
    tetmesh2 = TetMesh.read_from_file('cube2.vol')
    mesh_composition('out.vol', tetmesh1, tetmesh2)


if __name__ == '__main__':
    main()
