from PyQt6.QtWidgets import QDialog

from assets.design_about import Ui_Dialog

class WindowAbout(QDialog):
    '''
    Окно с информацией о технических характеристиках программы
    '''
    def __init__(self, parent=None):
        super(WindowAbout, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
