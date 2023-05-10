from mesh.tetmesh import TetMesh
from utils.mesh_merger import merge_meshes
from utils.mesh_writer import write_mesh_to_file


def main():
    tetmesh1 = TetMesh.read_from_file('cube.vol')
    tetmesh2 = TetMesh.read_from_file('cube2.vol')
    surface_number1 = 5
    surface_number2 = 6
    tetmesh = merge_meshes(surface_number1, surface_number2, tetmesh1, tetmesh2)
    write_mesh_to_file('out.vol', tetmesh)
    # merge_meshes(surface_number1, surface_number2, tetmesh1, tetmesh2)


if __name__ == '__main__':
    main()
