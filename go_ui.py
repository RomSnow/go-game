import sys

from PyQt5 import QtWidgets

from graphics.main_window import MainWindow


def main():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
