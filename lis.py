# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *
import math


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 280)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(60, 60, 370, 50))
        self.textEdit.setObjectName("origin sequence")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(470, 60, 130, 50))
        self.pushButton.setObjectName("start")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(60, 140, 370, 50))
        self.textEdit_2.setObjectName("subsequence")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.start)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "最长单调递增子序列"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "请输入空格间隔、由数字组成的字符串，例如 0 1 2"))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "最长递增子序列"))
        self.pushButton.setText(_translate("MainWindow", "计算"))

    def start(self):
        array = self.textEdit.toPlainText().split()
        result = self.cal_lis(array)
        self.textEdit_2.setPlainText(" ".join(result))
        return

    def binsearch(self, array, target, low, high):
        while high > low:
            mid = math.floor((low + high) / 2)
            if target < array[mid]:
                high = mid
            else:
                low = mid + 1
        return low

    def cal_lis(self, array):
        L = []
        substrtail = [0] * len(array)
        for i in range(len(array)):
            rank = self.binsearch(L, array[i], 0, len(L))
            if rank == 0:
                if len(L) == 0:
                    L.append(array[i])
                else:
                    L[rank] = array[i]
                substrtail[i] = rank + 1
            elif rank == len(L):
                if L[rank - 1] < array[i]:
                    L.append(array[i])
                    substrtail[i] = rank + 1
                else:
                    substrtail[i] = rank
            elif L[rank - 1] < array[i]:
                L[rank] = array[i]
                substrtail[i] = rank + 1
            else:
                substrtail[i] = rank

        chain = 1
        substr = []
        for i in range(len(substrtail)):
            if substrtail[i] == chain:
                substr.append(array[i])
                chain += 1

        return substr


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
