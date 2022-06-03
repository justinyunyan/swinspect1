import os
import sys
import threading
import time
import math

from UI1 import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


class PyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ini_table()
        self.show()
        self.Moveup_bt.clicked.connect(lambda: self.move_up())
        self.data_maping = {"啟用", "名稱", "值", "公差類型", "上限", "下限", "區域", "X", "Y", "ORI"}

    def set_checkbox_trigger(self, i):
        return self.item_list[i][0][0].stateChanged.connect(lambda: self.write_check_status(i))

    def ini_table(self):

        self.item_list = []
        self.checkbox_list = []
        item_paras = []

        with open(r"C:\temp\swinspect.txt", "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line != "//":
                    item_paras.append(line)
                else:
                    self.item_list.append(item_paras)
                    col_count = len(item_paras)
                    item_paras = []

        row_count = len(self.item_list)
        self.tableWidget.setColumnCount(col_count)  # minus count = data not show to user
        self.tableWidget.setRowCount(len(self.item_list))
        _translate = QtCore.QCoreApplication.translate
        tol_type = ["無", "基本", "雙向公差", "上下極限", "對稱", "MIN", "MAX"]

##Set Column
        for i in range(col_count):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        self.tableWidget.horizontalHeaderItem(0).setText(_translate("MainWindow", "啟用"))
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.horizontalHeaderItem(1).setText(_translate("MainWindow", "名稱"))
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.horizontalHeaderItem(2).setText(_translate("MainWindow", "值"))
        self.tableWidget.horizontalHeaderItem(3).setText(_translate("MainWindow", "公差類型"))
        self.tableWidget.horizontalHeaderItem(4).setText(_translate("MainWindow", "上限"))
        self.tableWidget.horizontalHeaderItem(5).setText(_translate("MainWindow", "下限"))
        self.tableWidget.horizontalHeaderItem(6).setText(_translate("MainWindow", "區域"))

##Set Row
        for i in range(row_count):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
            self.tableWidget.verticalHeaderItem(i).setText(_translate("MainWindow", str(i + 1)))

            self.combobox = QtWidgets.QComboBox()
            self.combobox.addItems(tol_type)
            self.tableWidget.setCellWidget(i, 4, self.combobox)


            self.layout = QHBoxLayout()
            a = QtWidgets.QCheckBox()
            self.item_list[i][0] = [a,self.item_list[i][0]]
            self.set_checkbox_trigger(i)
            self.layout.addWidget(a)
            self.layout.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.setContentsMargins(0, 0, 0, 0);
            self.mywidget = QWidget()
            self.mywidget.setLayout(self.layout)
            self.tableWidget.setCellWidget(i, 0, self.mywidget)

##Set cell
        for i in range(row_count):
            for j in range(col_count):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)
        self.fill_table()

    def write_check_status(self,a):

        print(a)

    def move_up(self):
        row_index = self.tableWidget.currentRow()
        col_index = self.tableWidget.currentColumn()
        if row_index != 0:
            a = self.item_list.pop(row_index)
            self.item_list.insert(row_index - 1, a)
            self.fill_table()
            self.tableWidget.clearSelection()
            self.tableWidget.setCurrentCell(row_index - 1, col_index)

    def fill_table(self):
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(self.item_list)):
            for j in range(len(self.item_list[i])):
                if j == 0:
                    a = self.tableWidget.cellWidget(i, 0)
                    a = a.children()
                    if self.item_list[i][j] == "0":
                        a[1].setChecked(False)
                    elif self.item_list[i][j] == "1":
                        a[1].setChecked(True)
                if j == 1:
                    self.tableWidget.item(i, 1).setText(_translate("MainWindow", self.item_list[i][j]))
                elif j == 5:
                    if "E-0" in self.item_list[i][j]:
                        a = self.item_list[i][j].split("E-0")
                        a = float(a[0]) * (10 ** (3 - int(a[1])))
                        self.tableWidget.item(i, 2).setText(_translate("MainWindow", "{:.2f}".format(a)))
                    else:
                        a = float(self.item_list[i][j]) * 1000
                        self.tableWidget.item(i, 2).setText(_translate("MainWindow", "{:.2f}".format(a)))
                elif j == 6:
                    self.tableWidget.item(i, 6).setText(_translate("MainWindow", self.item_list[i][j]))
                elif j == 7:
                    a = self.tableWidget.cellWidget(i, 4)
                    a.setCurrentIndex(int(self.item_list[i][j]))


app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = PyMainWindow()
ui.show()
sys.exit(app.exec_())
