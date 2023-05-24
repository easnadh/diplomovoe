from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from ui.ui_converter import UiConvert
from ui.ui_merger import UiMerge


class UiMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(r'C:\Users\first\PycharmProjects\diplomovoe\ui\ui_menu.ui', self)
        self.merge_meshes_button.clicked.connect(self.open_ui_merge)
        self.convert_extension_button.clicked.connect(self.open_ui_convert)
        self.setWindowIcon(QIcon(r'C:\Users\first\PycharmProjects\diplomovoe\ui\mesh.ico'))

    def open_ui_merge(self):
        self.ui_merge = UiMerge()
        self.ui_merge.show()

    def open_ui_convert(self):
        self.ui_convert = UiConvert()
        self.ui_convert.show()
