from PyQt5 import QtWidgets

from FrontEnd.UIWindow import UIWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = UIWindow()  # Se crea y se configura la ventana
    window.show()  # Se muestra la ventana
    app.exec()