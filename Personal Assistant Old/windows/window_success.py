from PyQt6.QtWidgets import QDialog

from assets.design_success import Ui_Dialog
from PyQt6 import QtCore

class WindowSuccess(QDialog):
    '''
    Окно с информацией об успешном сохранении информации
    '''
    def __init__(self, parent=None):
        super(WindowSuccess, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.ui.buttonBox.clicked.connect(self.close_window)

    def close_window(self):
        self.close()
        