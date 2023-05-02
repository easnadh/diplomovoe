from mesh.tetmesh import TetMesh
from utils.mesh_merger import merge_meshes


def main():
    tetmesh = TetMesh.read_from_file('cube.vol')
    tetmesh2 = TetMesh.read_from_file('cube2.vol')
    merge_meshes('dump.vol', tetmesh, tetmesh2)


if __name__ == '__main__':
    main()
