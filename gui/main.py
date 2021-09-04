from PyQt5 import QtWidgets
from Sources.mainWindow import Ui_MainWindow
from Sources.LoginDialog import Ui_Dialog
from Sources.DialogAdd import Ui_Dialog as AddUi_Dialog
from Sources.DialogDelete import Ui_Dialog as DelUi_Dialog
from Sources.DialogEdit import Ui_Dialog as EdiUi_Dialog

from pprint import pprint
import  misc
import sys


class mainWindow(QtWidgets.QMainWindow):

    actions = {}

    def __init__(self, parent, conn):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.parent = parent
        self.conn = conn
        self.cursor = conn.cursor()
        self.createActions()

        self.ui.menubar.addAction(self.actions['exitAction'])

        self.ui.btnCreate.clicked.connect(self.openAddDialog)
        self.ui.btnDelete.clicked.connect(self.openDelDialog)
        self.ui.btnEdit.clicked.connect(self.openEditDialog)

        self.ui.btnStatistic.setVisible(False)
        self.ui.btnStatistic.clicked.connect(self.showMonthlyShopSums)

        self.ui.tableWidget.cellDoubleClicked.connect(self.showOrderInfo)
        self.ui.widgControl.setVisible(False)

        self.ui.btnBack.setVisible(False)
        self.ui.btnBack.clicked.connect(self.showOrders)

        self.itemToUpdate = ''

        query = 'select session_user;'

        result = misc.selectFromBD(self.cursor, query)
        self.userRole = result[0][0]

        if self.userRole == 'genmanager':
            dicts = self.ui.menubar.addMenu('Справочники')
            dicts.addAction(self.actions['ingrs'])
            dicts.addAction(self.actions['products'])
            dicts.addAction(self.actions['customers'])

        self.ui.menubar.addAction(self.actions['orders'])

        self.senders = ['order', 'ing', 'customer', 'product', 'ingInPr', 'prInOrd']
        self.currentSender = ''

        
    def createActions(self):
        '''
        Создаёт обработчики для пунктов меню
        :return:
        '''
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
        '''
        Проверяет роль пользователя в текущей сессии

        :return:
        '''

        query = 'SELECT session_user;'
        res = misc.selectFromBD(self.cursor, query)


    def closeEvent(self, event):
        '''
        Переопределение метода закрытия окна

        :param event:
        :return:
        '''
        if self.conn != None : self.conn.close()

        self.destroy()
        self.parent.show()


    def fillTable(self, tableWidg, labels, items):
       '''
       Заполняет таблицу данными

       :param tableWidg: таблица, которую нужно заполнить
       :param labels: список заголовков столбцов
       :param items: данные
       :return:
       '''
       tableWidg.setRowCount(0)

       tableWidg.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
       tableWidg.setColumnCount(len(labels))
       tableWidg.setHorizontalHeaderLabels(labels)

       try:
           tableWidg.cellDoubleClicked.disconnect()
       except:
           pass

       if labels[0]=='№ заказа':
            tableWidg.cellDoubleClicked.connect(self.showOrderInfo)
       elif labels[0] =='Нaзвание':
            tableWidg.cellDoubleClicked.connect(self.showProductInfo)

       for item in items:
           row = tableWidg.rowCount()
           tableWidg.setRowCount(row+1)

           for i in range(len(item)):
             tableWidg.setItem(row, i, QtWidgets.QTableWidgetItem(str(item[i])))

    def openAddDialog(self):

        dialog = addDialog(self.conn, self.currentSender, self.itemToUpdate)
        dialog.exec()
        self.updateWindow()

    def openDelDialog(self):

        try:
            item = self.prepareRow()

            dialog = delDialog(self.conn, self.currentSender, item, self.itemToUpdate)
            dialog.exec()
            self.updateWindow()

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неправильный диапозон')
            msg.setWindowTitle("Ошибка выделения")
            msg.exec_()

    def openEditDialog(self):

        try:
            item = self.prepareRow()

            dialog = ediDialog(self.conn, self.currentSender, item, self.itemToUpdate)
            dialog.exec()
            self.updateWindow()

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неправильный диапозон')
            msg.setWindowTitle("Ошибка выделения")
            msg.exec_()


    def prepareRow(self):

        rows = self.ui.tableWidget.selectedIndexes()
        if len(rows) > 1: raise Exception('Выделено больше одного объекта')
        row = rows[0].row()

        return self.getRow(row)

    def getRow(self, row):

        item = []

        for i in range(self.ui.tableWidget.columnCount()):
            item.append(self.ui.tableWidget.item(row, i).text())

        return item


    def updateWindow(self):

        if self.currentSender == self.senders[0]:
            self.showOrders()
        elif self.currentSender == self.senders[1]:
            self.showIngrs()
        elif self.currentSender == self.senders[2]:
            self.showCustomers()
        elif self.currentSender == self.senders[3]:
            self.showProducts()
        elif self.currentSender == self.senders[4]:
            self.showProducts()
        else:
            self.showOrders()


    def showOrderInfo(self, row, column):
        '''
        Реакция на двойной клик по ячейке в таблице с заказами
        :param row: строка
        :param column: колонка
        :return:
        '''
        id = self.ui.tableWidget.item(row,0).text()
        self.ui.btnBack.setVisible(True)
        self.ui.btnBack.disconnect()
        self.ui.btnBack.clicked.connect(self.showOrders)
        self.ui.btnStatistic.setVisible(False)

        self.currentSender = self.senders[5]

        self.itemToUpdate = self.ui.tableWidget.item(row,0).text()

        query = 'select product, productAmount, price, totalPrice from allProductsInOrder where orderId = {0}'.format(id)
        result = misc.selectFromBD(self.cursor, query)
        labels = ['Продукт', 'Кол-во', 'Цена', 'Итоговая цена']

        self.fillTable(self.ui.tableWidget, labels, result)

    def showProductInfo(self, row, column):
        name = self.ui.tableWidget.item(row, 0).text()
        self.ui.btnBack.setVisible(True)
        self.ui.btnBack.disconnect()
        self.ui.btnStatistic.setVisible(False)
        self.ui.btnBack.clicked.connect(self.showProducts)

        self.currentSender = self.senders[4]

        query = "select id from Product where name = '{0}'".format(self.ui.tableWidget.item(row,0).text())
        result = misc.selectFromBD(self.cursor, query)
        self.itemToUpdate = result[0][0]

        query = "select ingredient, ingAmount, info from allIngsInProduct where product = '{0}'".format(name)
        result = misc.selectFromBD(self.cursor, query)
        labels = ['Ингридиент', 'Кол-во', 'Информация']

        self.fillTable(self.ui.tableWidget, labels, result)

    def showIngrs(self):
        '''
        Подготовка отображения раздела с ингридиентами
        :return:
        '''
        self.ui.widgControl.setVisible(True)
        self.ui.btnStatistic.disconnect()
        self.ui.btnStatistic.setVisible(True)
        self.ui.btnStatistic.setText('Топ 5 по месяцам')
        self.ui.btnStatistic.clicked.connect(self.showTop5)

        self.currentSender = self.senders[1]

        query = 'select * from allIngredients;'
        result = misc.selectFromBD(self.cursor, query)
        labels = ['Название', 'Цена', 'Информация']
        self.fillTable(self.ui.tableWidget,labels, result)

    def showTop5(self):
        '''
        Подготовка отображения раздела со статистической задачей
        :return:
        '''
        self.ui.widgControl.setVisible(False)
        self.ui.btnBack.setVisible(True)
        self.ui.btnStatistic.setVisible(False)

        self.ui.btnBack.clicked.connect(self.showIngrs)

        query = 'select * from Top5IngsMonthly'
        result = misc.selectFromBD(self.cursor, query)
        labels = ['Месяц', 'Продукты']
        self.fillTable(self.ui.tableWidget, labels, result)

    def showOrders(self):
        '''
        Подготовка отображения раздела с заказами
        :return:
        '''
        self.ui.widgControl.setVisible(True)
        self.ui.btnBack.setVisible(False)
        self.currentSender = self.senders[0]

        if self.userRole == 'genmanager':
            self.ui.btnStatistic.setVisible(True)
            self.ui.btnStatistic.disconnect()
            self.ui.btnStatistic.setText('Средние суммы')
            self.ui.btnBack.setVisible(False)
            self.ui.btnStatistic.clicked.connect(self.showMonthlyShopSums)


        query = 'select * from allOrders order by date;'
        result = misc.selectFromBD(self.cursor, query)
        labels = ['№ заказа', 'Компания', 'Дата', 'Статус', 'Цена']
        self.fillTable(self.ui.tableWidget,labels, result)

    def showMonthlyShopSums(self):
        '''
        Подготовка отображения раздела со статистической задачей
        :return:
        '''
        self.ui.widgControl.setVisible(False)
        self.ui.btnBack.setVisible(True)
        self.ui.btnStatistic.setVisible(False)

        self.ui.btnBack.clicked.connect(self.showOrders)

        query = 'select * from ShopAvrgOrderMonthly order by month;'
        result = misc.selectFromBD(self.cursor, query)
        labels = ['Заказчик', 'Месяц', 'Средняя сумма']
        self.fillTable(self.ui.tableWidget, labels, result)

    def showProducts(self):
        '''
        Подготовка отображения раздела с продуктами
        :return:
        '''
        self.ui.widgControl.setVisible(True)
        self.ui.btnStatistic.disconnect()
        self.ui.btnBack.setVisible(False)
        self.ui.btnStatistic.setVisible(True)
        self.ui.btnStatistic.setText('Топ продуктов')
        self.ui.btnStatistic.clicked.connect(self.showDemandedProduct)

        self.currentSender = self.senders[3]

        query = 'select * from allProducts;'
        result = misc.selectFromBD(self.cursor, query)
        # англ a
        labels = ['Нaзвание', 'Цена', 'Информация']
        self.fillTable(self.ui.tableWidget,labels, result)


    def showDemandedProduct(self):
        '''
        Подготовка отображения раздела со статистической задачей
        :return:
        '''
        self.ui.widgControl.setVisible(False)
        self.ui.btnBack.setVisible(True)
        self.ui.btnStatistic.setVisible(False)

        self.ui.btnBack.clicked.connect(self.showProducts)

        query = 'select * from DemandedProductMonthly;'
        result = misc.selectFromBD(self.cursor, query)
        labels = ['Месяц', 'Продукт', 'Количество добавлений']
        self.fillTable(self.ui.tableWidget, labels, result)

    def showCustomers(self):
        '''
        Подготовка отображения раздела с заказчиками
        :return:
        '''
        self.currentSender = self.senders[2]

        self.ui.widgControl.setVisible(True)
        self.ui.btnStatistic.setVisible(False)
        query = 'select * from allCustomers;'
        result = misc.selectFromBD(self.cursor, query)
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
        '''
        Вход в систему
        :return:
        '''

        userName = self.ui.lineUser.text()
        userPassw = self.ui.linePassword.text()

        try:

            self.conn = misc.connect(userName, userPassw)
            self.main = mainWindow(self, self.conn)

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
        '''
        Переопределение метода закрытия окна

        :param event:
        :return:
        '''

        self.destroy()
        self.close()


class addDialog(QtWidgets.QDialog):

    def __init__(self, conn, sender, itemId):
        super(addDialog, self).__init__()
        self.ui = AddUi_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Добавить')

        widgets =  { 'customer': self.ui.widgAddCustomer,
                     'ing': self.ui.widgetAddIng,
                     'product': self.ui.widgetProduct,
                     'ingInPr': self.ui.widgetIngInPrd,
                     'order': self.ui.widgetOrder,
                     'prInOrd': self.ui.widgetPrdInOrd
                   }

        self.currentSender = sender
        widgets[sender].setVisible(True)

        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.btnAdd.clicked.connect(self.addInfo)
        self.itemId = itemId
        self.conn = conn

        self.prepareComboBox()

    def prepareComboBox(self):

        query = ''
        cur = self.conn.cursor()
        result = []

        if self.currentSender == 'ingInPr':

            query = 'select name from allIngredients'
            result = misc.selectFromBD(cur, query)

            for item in result:
              self.ui.comboBoxIng.addItem(str(item[0]))

        elif self.currentSender == 'order':

            query = 'select name from Customer'
            result = misc.selectFromBD(cur, query)

            for item in result:
              self.ui.comboBoxCompany.addItem(str(item[0]))

            for state in ['not in stock', 'in stock', 'shipped', 'returned to warehouse', 'shipment cancellation']:
                self.ui.comboBoxState.addItem(state)

        elif self.currentSender == 'prInOrd':

            query = 'select name from allProducts'
            result = misc.selectFromBD(cur, query)

            for item in result:
              self.ui.comboBoxProd.addItem(str(item[0]))

        cur.close()

    def addInfo(self):

        query = ''

        if self.currentSender == 'customer':

            items = [self.ui.lineCompany, self.ui.linePhone]
            info = self.getText(items)

            query = "Call CustomerInsert('{0}','{1}');".format(info[0], info[1]) if len(info)!=0 else 'error'
        elif self.currentSender == 'ing':

            items = [self.ui.lineIngName, self.ui.lineIngPrice, self.ui.lineIngInfo]
            info = self.getText(items)

            query = "Call IngInsert('{0}','{1}','{2}');".format(info[0], info[1], info[2]) if len(info)!=0 else 'error'
        elif self.currentSender == 'product':

            items = [self.ui.lineProdName, self.ui.lineProdInfo]
            info = self.getText(items)

            query = "Call ProductInsert('{0}','{1}');".format(info[0], info[1]) if len(info) != 0 else 'error'
        elif self.currentSender == 'ingInPr':

            items = [self.ui.comboBoxIng, self.ui.lineAmountIng]
            info = self.getText(items)

            cur = self.conn.cursor()
            query = "select id from Ingredient where name = '{0}'".format(info[0])
            result = misc.selectFromBD(cur, query)
            cur.close()

            currentInfo =[self.itemId, result[0][0], info[1]]

            query = "Call PHIInsertUpdate({0},{1},{2});".format(currentInfo[0], currentInfo[1], currentInfo[2])
        elif self.currentSender == 'order':

            items = [self.ui.comboBoxCompany, self.ui.dateEdit, self.ui.comboBoxState]
            info = self.getText(items)

            cur = self.conn.cursor()
            query = "select id from Customer where name = '{0}'".format(info[0])
            result = misc.selectFromBD(cur, query)
            cur.close()

            currentInfo = [result[0][0], info[1], info[2]]

            query = "Call OrderInsert({0},'{1}','{2}');".format(currentInfo[0], currentInfo[1], currentInfo[2])
        elif self.currentSender == 'prInOrd':

            items = [self.ui.comboBoxProd, self.ui.lineAmountProd]
            info = self.getText(items)

            cur = self.conn.cursor()
            query = "select id from Product where name = '{0}'".format(info[0])
            result = misc.selectFromBD(cur, query)
            cur.close()

            currentInfo = [self.itemId, result[0][0], info[1]]

            query = "Call OHPInsertUpdate({0},{1},{2});".format(currentInfo[0], currentInfo[1], currentInfo[2])



        try:
            if query == 'error' or query == '': raise Exception()
            misc.transaction(self.conn, query)
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неправильный запрос')
            msg.setWindowTitle("Ошибка запроса")
            msg.exec_()

        self.close()

    def getText(self, items):

        info = []
        try:
            for item in items:

                if isinstance(item, QtWidgets.QComboBox):
                    text = item.currentText()
                elif isinstance(item, QtWidgets.QDateEdit):
                    text = item.date().toPyDate()
                else:
                    text = item.text()
                info.append(text)
                if text == '': raise Exception()

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Не все поля заполнены')
            msg.setWindowTitle("Ошибка заполнения")
            msg.exec_()

        return info


class delDialog(QtWidgets.QDialog):

    def __init__(self, conn, sender, item, parentItem):
        super(delDialog, self).__init__()
        self.ui = DelUi_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Удалить')

        self.ui.labelInfo.setText('Удалить {0}?'.format(item[0]))

        self.ui.btnNo.clicked.connect(self.close)
        self.ui.btnYes.clicked.connect(self.deleteInfo)

        self.conn = conn
        self.parentItem = parentItem
        self.currentSender = sender
        self.item = item

    def deleteInfo(self):

       if self.currentSender == 'customer':
           query = "Call CustomerDelete('{0}');".format(self.item[0]) if len(self.item) != 0 else 'error'
       elif self.currentSender == 'order':
           query = "Call OrdersDelete('{0}');".format(self.item[0]) if len(self.item) != 0 else 'error'
       elif self.currentSender == 'ing':
           query = "Call IngDelete('{0}');".format(self.item[0]) if len(self.item) != 0 else 'error'
       elif self.currentSender == 'product':
           query = "Call ProductDelete('{0}');".format(self.item[0]) if len(self.item) != 0 else 'error'
       elif self.currentSender == 'order':
           query = "Call OrdersDelete({0})".format(self.item[0]) if len(self.item) != 0 else 'error'
       elif self.currentSender == 'ingInPr':

           cur = self.conn.cursor()
           query = "select id from Ingredient where name = '{0}'".format(self.item[0])
           result = misc.selectFromBD(cur, query)

           query = "Call PHIDelete({0}, {1});".format(self.parentItem, result[0][0])
       elif self.currentSender == 'prInOrd':
           cur = self.conn.cursor()
           query = "select id from Product where name = '{0}'".format(self.item[0])
           result = misc.selectFromBD(cur, query)

           query = "Call OHPDelete({0}, {1});".format(self.parentItem, result[0][0])


       try:
           if query == 'error' or query == '': raise Exception()
           misc.transaction(self.conn, query)
       except:
           msg = QtWidgets.QMessageBox()
           msg.setIcon(QtWidgets.QMessageBox.Critical)
           msg.setText("Ошибка")
           msg.setInformativeText('Неправильный запрос')
           msg.setWindowTitle("Ошибка запроса")
           msg.exec_()

       self.close()

class ediDialog(QtWidgets.QDialog):

    def __init__(self, conn, sender, item, parentItem):
        super(ediDialog, self).__init__()
        self.ui = EdiUi_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Изменить')

        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.btnEdit.clicked.connect(self.editInfo)

        self.conn = conn
        self.currentSender = sender
        self.item = item
        self.parentItem = parentItem

        widgets =  { 'customer' : self.ui.widgCustomer,
                     'ing': self.ui.widgetAddIng,
                     'product': self.ui.widgetProduct,
                     'ingInPr': self.ui.widgetIngInPrd,
                     'order': self.ui.widgetOrder,
                     'prInOrd': self.ui.widgetPrdInOrd
                   }

        widgets[sender].setVisible(True)
        self.prepareComboBox()


    def prepareComboBox(self):

        query = ''
        cur = self.conn.cursor()
        result = []

        if self.currentSender == 'order':

            query = 'select name from Customer'
            result = misc.selectFromBD(cur, query)

            for item in result:
                self.ui.comboBoxCompany.addItem(str(item[0]))

            for state in ['not in stock', 'in stock', 'shipped', 'returned to warehouse', 'shipment cancellation']:
                self.ui.comboBoxState.addItem(state)

        cur.close()

    def editInfo(self):
        query = ''

        if self.currentSender == 'customer':
            items = [self.ui.lineCompany, self.ui.linePhone]
            info = self.getText(items)

            query = "Call CustomerUpdate('{0}','{1}', '{2}');".format(self.item[0], info[0], info[1]) if len(info) != 0 else 'error'

        elif self.currentSender == 'ing':

            items = [self.ui.lineIngName, self.ui.lineIngPrice, self.ui.lineIngInfo]
            info = self.getText(items)

            query = "Call IngUpdate('{0}','{1}','{2}','{3}');".format(self.item[0], info[0], info[1], info[2]) if len(info)!=0 else 'error'

        elif self.currentSender == 'product':
            items = [self.ui.lineProdName, self.ui.lineProdInfo]
            info = self.getText(items)

            query = "Call ProductUpdate('{0}','{1}','{2}');".format(self.item[0], info[0], info[1]) if len(info) != 0 else 'error'

        elif self.currentSender == 'order':
            items = [self.ui.comboBoxCompany, self.ui.dateEdit, self.ui.comboBoxState]
            info = self.getText(items)

            cur = self.conn.cursor()
            query = "select id from Customer where name = '{0}'".format(info[0])
            result = misc.selectFromBD(cur, query)
            cur.close()

            currentInfo = [self.item[0], result[0][0], info[1], info[2]]

            query = "Call OrderUpdate({0},{1},'{2}','{3}');".format(currentInfo[0], currentInfo[1], currentInfo[2], currentInfo[3])

        elif self.currentSender == 'ingInPr':

            items = [self.ui.lineAmountIng]
            info = self.getText(items)

            cur = self.conn.cursor()

            query = "select id from Ingredient where name = '{0}'".format(self.item[0])
            result = misc.selectFromBD(cur, query)

            cur.close()

            currentInfo =[self.parentItem, result[0][0], info[0]]

            query = "Call PHIDelete({0}, {1});".format(currentInfo[0], currentInfo[1])
            misc.transaction(self.conn, query)

            query = "Call PHIInsertUpdate({0},{1},{2});".format(currentInfo[0], currentInfo[1], currentInfo[2])

        elif self.currentSender == 'prInOrd':

            items = [self.ui.lineAmountProd]
            info = self.getText(items)

            cur = self.conn.cursor()

            query = "select id from Product where name = '{0}'".format(self.item[0])
            result = misc.selectFromBD(cur, query)

            cur.close()

            currentInfo = [self.parentItem, result[0][0], info[0]]

            query = "Call OHPDelete({0}, {1});".format(currentInfo[0], currentInfo[1])
            misc.transaction(self.conn, query)

            query = "Call OHPInsertUpdate({0},{1},{2});".format(currentInfo[0], currentInfo[1], currentInfo[2])


        try:
            if query == 'error' or query == '': raise Exception()
            misc.transaction(self.conn, query)
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неправильный запрос')
            msg.setWindowTitle("Ошибка запроса")
            msg.exec_()

        self.close()


    def getText(self, items):

        info = []

        for i in range(len(items)):
            if isinstance(items[i], QtWidgets.QComboBox):
                text = items[i].currentText()
            else:
                text = items[i].text()
            if text == '': text = self.item[i]
            info.append(text)

        return info


app = QtWidgets.QApplication([])
application = loginDialog()
application.show()

sys.exit(app.exec())

