import os
from datetime import datetime
from windows.check_engeneer import check_engeneer_info, check_engeneer_info_start

from PyQt6.QtWidgets import QDialog

from windows.window_success import WindowSuccess
from assets.design_info import Ui_Dialog
from windows.window_warning import WindowWarning

class WindowInfo(QDialog):
    '''
    Окно с информацией о текущей смены для инженера 
    '''
    def __init__(self, parent=None):
        super(WindowInfo, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.window_warning = WindowWarning()
        self.window_success = WindowSuccess()

        try: 
            with open("./данные/изменения_в_работе.txt", "r", encoding="utf-8") as file:
                self.ui.text_field.insertPlainText(f"{file.read()}")
        except Exception:
            self.window_warning.show()
            
        self.file_info()
        self.ui.label_person.setText(check_engeneer_info_start())
        self.ui.btn_save.clicked.connect(self.save_info)

    def file_info(self):
        try:
            filename = "./данные/изменения_в_работе.txt"
            res = os.path.getmtime(filename)
            new_date = datetime.fromtimestamp(res).strftime("%d.%m.%Y %H:%M")
            self.ui.label_date.setText(f"{new_date}")
        except Exception:
            self.window_warning.show()
    
    def save_info(self):
        try:
            with open("./данные/изменения_в_работе.txt", "w", encoding="utf-8") as file:
                text = self.ui.text_field.toPlainText()
                file.write(text)
                self.file_info()
                self.ui.label_person.setText(check_engeneer_info())
        except Exception:
            self.window_warning.show()
        else:
            self.window_success.show()
