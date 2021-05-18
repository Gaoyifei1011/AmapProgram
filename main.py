import sys

from PyQt5 import QtWidgets

from LoginMainWindow import LoginMainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = LoginMainWindow()
    loginWindow.show()
    sys.exit(app.exec_())
