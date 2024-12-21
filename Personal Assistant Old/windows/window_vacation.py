import json
from datetime import datetime

from PyQt6.QtWidgets import QDialog

from windows.window_update import WindowUpdate
from windows.window_success import WindowSuccess
from assets.design_vacation import Ui_Dialog
from windows.window_warning import WindowWarning

class WindowVacation(QDialog):
    '''
    Окно с графиками отпусков сотрудников 
    '''
    def __init__(self, parent=None):
        super(WindowVacation, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.list_person = (self.ui.text_field_1, self.ui.text_field_2,
                              self.ui.text_field_3, self.ui.text_field_4,
                              self.ui.text_field_5, self.ui.text_field_6)
        self.list_before = (self.ui.date_left_1, self.ui.date_left_2,
                            self.ui.date_left_3, self.ui.date_left_4,
                            self.ui.date_left_5, self.ui.date_left_6)
        self.list_after = (self.ui.date_right_1, self.ui.date_right_2,
                            self.ui.date_right_3, self.ui.date_right_4,
                            self.ui.date_right_5, self.ui.date_right_6)
        self.window_success = WindowSuccess()
        self.window_update = WindowUpdate()
        self.window_warning = WindowWarning()
        self.loading()
        self.ui.btn_save.clicked.connect(self.save_info)
        self.ui.btn_update_vacation.clicked.connect(self.update_info)

    def save_info(self):
        try:
            with (open("./данные/график_отпусков.json", "w", encoding="utf-8")
                as file):
                data = {}
                for person, before, after in zip(self.list_person,
                                                    self.list_before,
                                                    self.list_after):
                    date_before = before.dateTime().toString().split()
                    date_after = after.dateTime().toString().split()
                    value_1 = f"{date_before[2]}.{date_before[1]}.{datetime.now().strftime('%y')} 08:00AM"
                    value_2 = f"{date_after[2]}.{date_after[1]}.{datetime.now().strftime('%y')} 08:00AM"
                    data[person.text()] = [value_1, value_2]
                json.dump(data, file)
        except Exception:
            self.window_warning.show()
        else:
            self.window_success.show()
    
    def update_info(self):
        self.loading()
        self.window_update.show()

    def loading(self):
        try:
            with open("./данные/график_отпусков.json", "r", encoding="utf-8") as file:
                file_content = file.read()
                templates = json.loads(file_content)
                for person, before, after, item in zip(self.list_person,
                                                    self.list_before,
                                                    self.list_after,
                                                    templates):
                    person.setText(item)
                    date_before = datetime.strptime(templates[item][0],
                                                    "%d.%b.%y %I:%M%p")
                    date_after = datetime.strptime(templates[item][1],
                                                "%d.%b.%y %I:%M%p")
                    before.setDateTime(date_before)
                    after.setDateTime(date_after)
        except Exception:
            self.window_warning.show()
            