from PyQt6.QtWidgets import QDialog

from assets.design_warning import Ui_Dialog
from PyQt6 import QtCore

class WindowWarning(QDialog):
    '''
    Окно с информацией об ошибках
    '''
    def __init__(self, parent=None):
        super(WindowWarning, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.ui.buttonBox.clicked.connect(self.close_window)

    def close_window(self):
        self.close()
        