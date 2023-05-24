import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

from mesh.tetmesh import TetMesh
from ui.ui_menu import UiMenu
from utils.mesh_merger import merge_meshes
from utils.mesh_writer import write_mesh_to_file


def main():
    app = QApplication(sys.argv)
    ui = UiMenu()
    ui.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

