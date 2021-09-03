from PyQt5 import QtWidgets
from Sources.mainWindow import Ui_MainWindow
from Sources.LoginDialog import Ui_Dialog
import psycopg2 as ps2
import sys


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Login.activeAction()


class loginDialog(QtWidgets.QDialog):

    def __init__(self):
        super(loginDialog, self).__init__()
        self.main = mainWindow()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle('Вход в систему')
        self.setModal(True)


        self.ui.btnLogin.clicked.connect(self.startApplication)

    def startApplication(self):

        userName = self.ui.lineUser.text()
        userPassw = self.ui.linePassword.text()

        print(userName, userPassw)

        try:
            conn = ps2.connect(dbname='IceCreamCompany', user= userName,
                               password=userPassw, host='localhost')
            self.destroy()
            self.main.show()
        except:

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Неправильный логин/пароль')
            msg.setWindowTitle("Ошибка входа")
            msg.exec_()



    def closeEvent(self, event):
        self.destroy()


app = QtWidgets.QApplication([])
application = loginDialog()
application.show()

sys.exit(app.exec())