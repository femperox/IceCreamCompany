# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnCreate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCreate.setGeometry(QtCore.QRect(10, 10, 71, 28))
        self.btnCreate.setObjectName("btnCreate")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 50, 791, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.btnBack = QtWidgets.QPushButton(self.centralwidget)
        self.btnBack.setGeometry(QtCore.QRect(380, 10, 31, 31))
        self.btnBack.setObjectName("btnBack")
        self.btnStatistic = QtWidgets.QPushButton(self.centralwidget)
        self.btnStatistic.setGeometry(QtCore.QRect(250, 10, 121, 28))
        self.btnStatistic.setObjectName("btnStatistic")
        self.btnEdit = QtWidgets.QPushButton(self.centralwidget)
        self.btnEdit.setGeometry(QtCore.QRect(90, 10, 71, 28))
        self.btnEdit.setObjectName("btnEdit")
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setGeometry(QtCore.QRect(170, 10, 71, 28))
        self.btnDelete.setObjectName("btnDelete")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Ings = QtWidgets.QAction(MainWindow)
        self.Ings.setObjectName("Ings")
        self.Products = QtWidgets.QAction(MainWindow)
        self.Products.setObjectName("Products")
        self.Customers = QtWidgets.QAction(MainWindow)
        self.Customers.setObjectName("Customers")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnCreate.setText(_translate("MainWindow", "Добавить"))
        self.btnBack.setText(_translate("MainWindow", "<-"))
        self.btnStatistic.setText(_translate("MainWindow", "Топ5 по месяцам"))
        self.btnEdit.setText(_translate("MainWindow", "Изменить"))
        self.btnDelete.setText(_translate("MainWindow", "Удалить"))
        self.Ings.setText(_translate("MainWindow", "Ингридиенты"))
        self.Products.setText(_translate("MainWindow", "Продукты"))
        self.Customers.setText(_translate("MainWindow", "Заказчики"))
