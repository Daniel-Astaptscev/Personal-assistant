import openpyxl
from datetime import datetime

from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6 import QtCore, QtGui

from windows.window_update import WindowUpdate
from assets.design_report_card import Ui_Dialog
from windows.window_warning import WindowWarning

class WindowReportCard(QDialog):
    '''
    Окно с таблицей смен дежурств инженеров 
    '''
    def __init__(self, parent=None):
        super(WindowReportCard, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.window_update = WindowUpdate()
        self.window_warning = WindowWarning()
        months = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь', 7: 'июль', 8: 'август', 9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}
        res = datetime.now().strftime('%m')
        self.ui.label_month.setText(f"{months[int(res)]}")
        self.loading()
        self.ui.btn_update_table.clicked.connect(self.show_window_update)

    def show_window_update(self):
        self.loading()
        self.window_update.show()

    def loading(self):
        try:
            wookbook = openpyxl.load_workbook("./данные/табель_сотрудников.xlsx")
            worksheet = wookbook.active
            days = [worksheet['B3':'AG3'], worksheet['B4':'AG4'], worksheet['B5':'AG5'], worksheet['B6':'AG6'], worksheet['B7':'AG7']]
            person_card = [[], [], [], [], []]
            current_month = datetime.now().strftime('%m %Y').split()
            num = 0
            for day in days:
                for cell in day:
                    for item in cell:
                        person_card[num].append(item.value)
                num += 1
            row = 0
            for person in person_card:
                for col in range(31):
                    try:
                        if col == 0:
                            item = QTableWidgetItem(f"{person[col]}")
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                            item.setBackground(QtGui.QColor(207, 210, 255))
                            self.ui.table_persons.setItem(row, col, item)
                            continue
                        else:
                            res = datetime(year=int(current_month[1]), month=int(current_month[0]), day=int(col))
                    except Exception:
                        continue
                    item = QTableWidgetItem(f"{person[col]}")
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    if res.isoweekday() == 6 or res.isoweekday() == 7:
                        item.setBackground(QtGui.QColor(207, 210, 255))
                    else:
                        item.setBackground(QtGui.QColor(225, 232, 255))
                    self.ui.table_persons.setItem(row, col, item)
                row += 1
            profile = []
            if len(profile)>0:
                profile.clear()
            for item in worksheet['A3':'A7']:
                profile.append(item[0].value)
            self.ui.table_persons.setVerticalHeaderLabels(profile)
        except Exception:
            self.window_warning.show()
