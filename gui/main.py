from PyQt5 import QtWidgets
from Sources.mainWindow import Ui_MainWindow
from Sources.LoginDialog import Ui_Dialog
from pprint import pprint
import  misc
import sys


    

class mainWindow(QtWidgets.QMainWindow):

    actions = {}

    def __init__(self, parent, conn, pasw):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.parent = parent
        self.conn = conn
        self.pasw = pasw
        self.cursor = conn.cursor()
        self.createActions()

        self.ui.menubar.addAction(self.actions['exitAction'])
        self.ui.btnTest.clicked.connect(self.showOrders)

        self.ui.btnTop5.setVisible(False)
        self.ui.btnTop5.clicked.connect(self.showTop5)
        self.ui.btnBack.setVisible(False)
        self.ui.btnBack.clicked.connect(self.showOrders)

        query = 'select session_user;'

        result = misc.selectFromBD(self.cursor, query)
        self.userRole = result[0][0]

        if self.userRole == 'genmanager':
            dicts = self.ui.menubar.addMenu('Справочники')
            dicts.addAction(self.actions['ingrs'])
            dicts.addAction(self.actions['products'])
            dicts.addAction(self.actions['customers'])

        self.ui.menubar.addAction(self.actions['orders'])

        
    def createActions(self):
        self.actions['exitAction'] = QtWidgets.QAction('&Выход', self)
        self.actions['exitAction'].setShortcut('Ctrl+Q')
        self.actions['exitAction'].triggered.connect(self.closeEvent)

        self.actions['orders'] = QtWidgets.QAction('&Заказы', self)
        self.actions['orders'].triggered.connect(self.showOrders)

        self.actions['ingrs'] = QtWidgets.QAction('&Ингридиенты', self)
        self.actions['ingrs'].triggered.connect(self.showIngrs)

        self.actions['products'] = QtWidgets.QAction('&Продукты', self)
        self.actions['products'].triggered.connect(self.showProducts)

        self.actions['customers'] = QtWidgets.QAction('&Заказчики', self)
        self.actions['customers'].triggered.connect(self.showCustomers)


    def checkRole(self):

        query = 'SELECT session_user;'
        res = misc.selectFromBD(self.cursor, query)

        print(res)


    def closeEvent(self, event):
        if self.conn != None : self.conn.close()

        self.destroy()
        self.parent.show()


    def fillTable(self, tableWidg, labels, items):
       tableWidg.setRowCount(0)

       tableWidg.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
       tableWidg.setColumnCount(len(labels))
       tableWidg.setHorizontalHeaderLabels(labels)

       tableWidg.cellDoubleClicked.connect(self.showNewTable)
       if labels[0] != '№ заказа':
           tableWidg.cellDoubleClicked.disconnect()

       for item in items:
           row = tableWidg.rowCount()
           tableWidg.setRowCount(row+1)

           for i in range(len(item)):
             tableWidg.setItem(row, i, QtWidgets.QTableWidgetItem(str(item[i])))


    def showNewTable(self, row, column):

        id = self.ui.tableWidget.item(row,0).text()

        #self.ui.tableWidgetMore.setVisible(True)
        self.ui.btnBack.setVisible(True)

        query = 'select product, productAmount, price, totalPrice from allProductsInOrder where orderId = {0}'.format(id)
        result = misc.selectFromBDWithConn(self.userRole, self.pasw, query)
        labels = ['Продукт', 'Кол-во', 'Цена', 'Итоговая цена']

        self.fillTable(self.ui.tableWidget, labels, result)


    def showIngrs(self):
        self.ui.btnTop5.setVisible(True)
        query = 'select * from allIngredients;'
        result = misc.selectFromBDWithConn(self.userRole, self.pasw, query)
        labels = ['Название', 'Цена', 'Информация']
        self.fillTable(self.ui.tableWidget,labels, result)

    def showTop5(self):
        self.ui.btnBack.setVisible(True)
        self.ui.btnTop5.setVisible(False)
        self.ui.btnBack.clicked.connect(self.showIngrs)

        query = 'select * from Top5IngsMonthly'
        result = misc.selectFromBDWithConn(self.userRole, self.pasw, query)
        labels = ['Месяц', 'Продукты']
        self.fillTable(self.ui.tableWidget, labels, result)

    def showOrders(self):
        self.ui.btnBack.setVisible(False)

        query = 'select * from allOrders order by date;'
        result = misc.selectFromBDWithConn(self.userRole, self.pasw, query)
        labels = ['№ заказа', 'Компания', 'Дата', 'Статус', 'Цена']
        self.fillTable(self.ui.tableWidget,labels, result)

    def showProducts(self):

        query = 'select * from allProducts;'
        result = misc.selectFromBDWithConn(self.userRole, self.pasw, query)
        labels = ['Название', 'Цена', 'Информация']
        self.fillTable(self.ui.tableWidget,labels, result)

    def showCustomers(self):

        query = 'select * from allCustomers;'
        result = misc.selectFromBDWithConn(self.userRole, self.pasw, query)
        labels = ['Компания', 'Телефон']
        self.fillTable(self.ui.tableWidget,labels, result)


class loginDialog(QtWidgets.QDialog):

    def __init__(self):
        super(loginDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.main = None
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
            self.main = mainWindow(self, self.conn, userPassw)

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

