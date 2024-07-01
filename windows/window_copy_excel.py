from win32com.client import Dispatch

from PyQt6.QtWidgets import QDialog
from PyQt6 import QtWidgets

from assets.design_copy_excel import Ui_LoadingPage
from windows.window_success import WindowSuccess
from windows.window_warning import WindowWarning

class WindowCopyExcel(QDialog):
    '''
    Окно для загрузки и копирования, потом перезаписи файла эксель
    '''
    def __init__(self, parent=None):
        super(WindowCopyExcel, self).__init__(parent)
        self.ui = Ui_LoadingPage()
        self.ui.setupUi(self)
        self.window_success = WindowSuccess()
        self.window_warning = WindowWarning()
        self.ui.btn_load.clicked.connect(self.loading)

    def loading(self):
        try:
            path_load = QtWidgets.QFileDialog.getOpenFileName(caption='Выбрать файл для загрузки')[0]
            path_save = QtWidgets.QFileDialog.getOpenFileName(caption='Выбрать файл для сохранения')[0]
            xl = Dispatch("Excel.Application")
            xl.visible=True
            book_load = xl.Workbooks.Open(Filename=path_load)
            book_save = xl.Workbooks.Open(Filename=path_save)
            sheet = book_load.ActiveSheet
            sheet.Copy(Before=book_save.ActiveSheet)
            book_save.Worksheets(2).Delete()
            book_load.Close(SaveChanges=False)
            book_save.Close(SaveChanges=True)
            xl.Quit()
        except Exception:
            self.window_warning.show()
        else:
            self.window_success.show()
