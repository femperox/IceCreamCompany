from PyQt5 import QtWidgets
from Sources.mainWindow import Ui_MainWindow
from Sources.LoginDialog import Ui_Dialog
from pprint import pprint
import  misc
import sys


    

class mainWindow(QtWidgets.QMainWindow):

    actions = {}
    cursor = None

    pasw = ""

    def __init__(self, parent):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.parent = parent
        self.conn = None
        self.userRole = None

        self.createActions()

        self.ui.menubar.addAction(self.actions['exitAction'])
        self.ui.btnTest.clicked.connect(self.showOrders)

        
    def createActions(self):
        self.actions['exitAction'] = QtWidgets.QAction('&Выход', self)
        self.actions['exitAction'].setShortcut('Ctrl+Q')
        self.actions['exitAction'].triggered.connect(self.closeEvent)

        self.actions['orders'] = QtWidgets.QAction('&Заказы', self)
        self.actions['orders'].triggered.connect(self.showOrders)


    def showOrders(self):

        query = 'select * from allOrders order by date;'
        result = misc.selectFromBDWithConn(self.userRole, self.pasw, query)
        labels = ['№ заказа', 'Компания', 'Дата', 'Статус', 'Цена']
        self.fillTable(labels, result)


    def checkRole(self):

        query = 'SELECT session_user;'
        res = misc.selectFromBD(self.cursor, query)

        print(res)


    def closeEvent(self, event):
        if self.conn != None : self.conn.close()

        self.destroy()
        self.parent.show()


    def update(self, conn, pasw):
        '''
        Обновляет параметры главного окна в зависимости от ролей
        :param conn:
        :return:
        '''

        self.conn = conn
        self.cursor = conn.cursor()
        self.pasw = pasw
        query = 'select session_user;'

        result = misc.selectFromBD(self.cursor, query)
        self.userRole = result[0][0]

        if self.userRole == 'genmanager':
            pass

        self.ui.menubar.addAction(self.actions['orders'])

        

    def fillTable(self, labels, items):

       self.ui.tableWidget.setColumnCount(len(labels))
       self.ui.tableWidget.setHorizontalHeaderLabels(labels)


       for item in items:
           row = self.ui.tableWidget.rowCount()
           self.ui.tableWidget.setRowCount(row+1)

           self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
           self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item[1]))
           self.ui.tableWidget.setItem(row, 2, QtWidgets. QTableWidgetItem(str(item[2])))
           self.ui.tableWidget.setItem(row, 3, QtWidgets. QTableWidgetItem(item[3]))
           self.ui.tableWidget.setItem(row, 4, QtWidgets. QTableWidgetItem(item[4]))

class loginDialog(QtWidgets.QDialog):

    def __init__(self):
        super(loginDialog, self).__init__()
        self.main = mainWindow(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle('Вход в систему')
        self.setModal(True)

        self.conn = None
        self.ui.btnLogin.clicked.connect(self.startApplication)

    def startApplication(self):

        userName = self.ui.lineUser.text()
        userPassw = self.ui.linePassword.text()

        try:
            self.conn = misc.connect(userName, userPassw)
            self.main.update(self.conn, userPassw)

            self.destroy()
            self.close()

            self.main.show()

        except:
            userPassw = self.ui.linePassword.setText('')

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неправильный логин/пароль')
            msg.setWindowTitle("Ошибка входа")
            msg.exec_()



    def closeEvent(self, event):

        if self.conn != None : self.conn.close()
        self.destroy()
        self.close()


app = QtWidgets.QApplication([])
application = loginDialog()
application.show()

sys.exit(app.exec())

