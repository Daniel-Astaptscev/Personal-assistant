from PyQt6.QtWidgets import QDialog

from assets.design_update import Ui_Dialog

class WindowUpdate(QDialog):
    '''
    Окно с уведомлением об успешном обновлении информации
    '''
    def __init__(self, parent=None):
        super(WindowUpdate, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.clicked.connect(self.close_window)

    def close_window(self):
        self.close()
