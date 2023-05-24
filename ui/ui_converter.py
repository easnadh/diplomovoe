from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.uic import loadUi

from exceptions.file_errors import *
from mesh.tetmesh import TetMesh
from utils.mesh_writer import write_mesh_to_file


class UiConvert(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(r'C:\Users\first\PycharmProjects\diplomovoe\ui\ui_converter.ui', self)
        self.load_mesh_file_button.clicked.connect(self.load_mesh_file)
        self.get_result_button.clicked.connect(self.get_result)
        self.setWindowIcon(QIcon(r'C:\Users\first\PycharmProjects\diplomovoe\ui\mesh.ico'))

    def load_mesh_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '*.vol; *.dat')
        self.mesh_lineedit.setText(file_name[0])

    def get_result(self):
        mesh = self.mesh_lineedit.text()

        if not mesh:
            msg = QMessageBox()
            msg.setText("Field can't be empty")
            msg.setWindowTitle('Error')
            msg.exec()
        else:
            tetmesh = self.check_and_read_file(mesh)
            if tetmesh:
                try:
                    file_name = QFileDialog.getSaveFileName(self, 'Save File', '*.vol; *.dat')
                    write_mesh_to_file(file_name[0], tetmesh)
                    if file_name[0]:
                        self.close()
                except ValueError as e:
                    self.error_label.setText(str(e))
                except FileExtensionError as e:
                    self.error_label.setText(str(e))

    def check_and_read_file(self, mesh):
        try:
            tetmesh = TetMesh.read_from_file(mesh)
            return tetmesh
        except FileExtensionError as e:
            self.error_label.setText(str(e))
        except FileStructureError as e:
            self.error_label.setText(str(e))
