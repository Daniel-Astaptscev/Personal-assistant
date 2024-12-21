import sys
import os
from datetime import datetime

from windows.temperature import calculate_temperature, saving_temperature
from windows.check_engeneer import check_engeneer
from apscheduler.schedulers.qt import QtScheduler

from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton
from PyQt6 import QtCore
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

from assets.design_main_window import Ui_MainWindow
from windows.window_success import WindowSuccess
from windows.window_info import WindowInfo
from windows.window_about import WindowAbout
from windows.window_update import WindowUpdate
from windows.window_vacation import WindowVacation
from windows.window_copy_excel import WindowCopyExcel
from windows.window_report_card import WindowReportCard
from windows.window_warning import WindowWarning

class WebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @pyqtSlot(QtCore.QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()

class MainWindow(QMainWindow):
    '''
    Главное окно при запуске программы с вкладками
    '''
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.color = True
        self.ui.btn_about.clicked.connect(self.open_about)
        self.ui.btn_copy_excel.clicked.connect(self.open_copy_excel)
        self.ui.btn_info.clicked.connect(self.open_info)
        self.ui.btn_delete.clicked.connect(self.action_delete)
        self.ui.btn_vacation.clicked.connect(self.open_vacation)
        self.area_checkbox = ((self.ui.checkbox_1, self.ui.text_checkbox_1), (self.ui.checkbox_2, self.ui.text_checkbox_2), (self.ui.checkbox_3, self.ui.text_checkbox_3), (self.ui.checkbox_4, self.ui.text_checkbox_4), (self.ui.checkbox_5, self.ui.text_checkbox_5), (self.ui.checkbox_6, self.ui.text_checkbox_6), (self.ui.checkbox_7, self.ui.text_checkbox_7), (self.ui.checkbox_8, self.ui.text_checkbox_8))
        self.ui.btn_start.clicked.connect(self.open_start)
        self.ui.btn_delete_log.clicked.connect(self.delete_log_file)
        self.ui.btn_profile.clicked.connect(self.open_report_card)
        self.ui.btn_search.clicked.connect(self.open_files)
        self.update_engeneer()
        self.ui.pushButton.clicked.connect(self.new_background)

        # Создание веб-страниц внутри главного окна на Tab-вкладках
        ###################################################################################################
        self.webEngineView_email = QWebEngineView()
        page_email = WebEnginePage(self.webEngineView_email)
        self.webEngineView_email.setPage(page_email)
        self.webEngineView_email.load(QUrl("https://yandex.ru/"))
        self.ui.TabWindow.insertTab(1, self.webEngineView_email, "Быстрый поиск")

        self.webEngineView_mka = QWebEngineView()
        page_mka = WebEnginePage(self.webEngineView_mka)
        self.webEngineView_mka.setPage(page_mka)
        self.webEngineView_mka.load(QUrl("https://аис.фрт.рф/"))
        self.ui.TabWindow.insertTab(2, self.webEngineView_mka, "МКА Реформа ЖКХ")

        self.webEngineView_server = QWebEngineView()
        page_server = WebEnginePage(self.webEngineView_server)
        self.webEngineView_server.setPage(page_server)
        self.webEngineView_server.load(QUrl("https://www.google.com/"))
        self.ui.TabWindow.insertTab(4, self.webEngineView_server, "Телеметрия")

        self.ui.webBook.load(QtCore.QUrl.fromLocalFile(r"C:\\Users\\User01\\Desktop\\Персональный помощник\\данные\\сайт\\site.html"))

        self.btn_home = QToolButton(self)
        self.btn_home.setFixedSize(QtCore.QSize(60, 21))
        self.btn_home.setStyleSheet("""*{margin-right: 20px}""")
        self.btn_home.setText("🌏")
        self.ui.TabWindow.setCornerWidget(self.btn_home)
        self.btn_home.clicked.connect(self.back_home)

        # Запуск задач на обновление инженеров ежедневно в 08:00
        ###################################################################################################
        scheduler = QtScheduler()
        scheduler.add_job(self.update_engeneer, 'cron', day_of_week='*',
                          hour=8, minute=0)
        scheduler.start()

        try: 
            with open("./данные/рабочая_область.txt", "r", encoding="utf-8") as file:
                self.ui.text_area.insertPlainText(f"{file.read()}")
        except Exception:
            window_warning.show()

    def new_background(self):
        if self.color:
            self.ui.text_area.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.color = False
        else:
            self.ui.text_area.setStyleSheet("background-color: rgb(225, 232, 255);")
            self.color = True
    def back_home(self):
        tab_text = self.ui.TabWindow.tabText(self.ui.TabWindow.currentIndex())
        if tab_text == "Быстрый поиск":
            self.webEngineView_email.load(QUrl("https://yandex.ru/"))
        elif tab_text == "Справочник":
            self.ui.webBook.load(QtCore.QUrl.fromLocalFile(r"C:\\Users\\User01\\Desktop\\Персональный помощник\\данные\\сайт\\site.html"))
        elif tab_text == "МКА Реформа ЖКХ":
            self.webEngineView_mka.load(QUrl("https://аис.фрт.рф/"))
        elif tab_text == "Телеметрия":
            self.webEngineView_server.load(QUrl("https://www.google.com/"))
    def update_engeneer(self):
        try:
            engeneer_1, engeneer_2 = check_engeneer()
            self.ui.label_employees.setText(f"{engeneer_1} / {engeneer_2}")
        except Exception:
            window_warning.show()

    def closeEvent(self, event):   
        try: 
            with open("./данные/рабочая_область.txt", "w", encoding="utf-8") as file:
                text = self.ui.text_area.toPlainText()
                file.write(text)
            QApplication.closeAllWindows()
            event.accept()
        except Exception:
            window_warning.show()
        else:
            window_success.show()

    def open_start(self):
        date = self.ui.date_input.dateTime()
        res_date = date.date()
        value = self.ui.value_input.value()
        bar_value = 4
        regions = ['isakly', 'koshki-samarskaya',
           'elhovka-elhovskiy-rayon-samarskaya',
           'verhnie-belozerki',
           'bolshaya-chernigovka',
           'pestravka', 'bezenchuk',
           'hvorostyanka-samarskaya',
           'lopatino-volzhskiy-rayon-samarskaya',
           'malaya-malyshevka', 'neftegorsk',
           'kinel-cherkassy',
           'pohvistnevo', 'Pohvistnevo',
           'otradniy', 'privolzhe-samarskaya',
           'chapaevsk', 'novokuybishevsk',
           'samara', 'zhigulevsk',
           'oktyabrsk', 'bayderyakovo-samarskaya',
           'Neftegorsk', 'bogatoe-samarskaya']
        self.ui.textEdit.insertPlainText(f"[{datetime.now()}] ЗАПУСК цикла выгрузки данных по погоде...\n")
        self.ui.progress_bar.setValue(bar_value) 
        for reg in regions:
            try:
                res = calculate_temperature(item=reg, year=res_date.year(), month=res_date.month(), fact_value=value)
                bar_value += 4
                self.ui.progress_bar.setValue(bar_value) 
                self.ui.textEdit.insertPlainText(res[0] + res[1]) 
            except Exception:
                self.ui.textEdit.insertPlainText('неизвестная ошибка - входные данные не могут быть обработаны...\n')
        if saving_temperature(year=res_date.year(), month=res_date.month(),
                            fact_value=value):
            self.ui.textEdit.insertPlainText(f"[{datetime.now()}] данные "
                                             f"успешно сохранены в "
                                             f"таблицу...\n")
        else:
            self.ui.textEdit.insertPlainText(f"[{datetime.now()}] непредвиденная ошибка: данные не внесены в таблицу...\n")
        self.ui.textEdit.insertPlainText(f"[{datetime.now()}] ОСТАНОВКА цикла...\n\n")

    def delete_log_file(self):
        self.ui.textEdit.clear()
        self.ui.progress_bar.setValue(0)

    def open_report_card(self):
        window_report_card.show()

    def open_about(self):
        window_about.show()

    def open_copy_excel(self):
        window_copy_excel.show()

    def open_info(self):    
        window_info.show()

    def open_vacation(self):    
        window_vacation.show()

    def open_files(self):
        try:
            path = r"C:\Users\User01\Desktop\Персональный Помощник"
            dir_path = QFileDialog.getOpenFileName(self, 'Выбрать файл для просмотра', path)
            if dir_path[0]:
                os.startfile(f'{dir_path[0]}')
        except Exception:
            window_warning.show()

    def action_delete(self):
        for value, item in enumerate(self.area_checkbox, start=1):
            if item[0].isChecked():
                item[0].setChecked(False)
                item[1].clear()
                item[1].insertPlainText(f"\nЗадача # {value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window_success = WindowSuccess()
    window_warning = WindowWarning()
    main_window = MainWindow()
    window_about = WindowAbout()
    window_copy_excel = WindowCopyExcel()
    window_info = WindowInfo()
    window_report_card = WindowReportCard()
    window_update = WindowUpdate()
    window_vacation = WindowVacation()

    main_window.show()

    sys.exit(app.exec())
