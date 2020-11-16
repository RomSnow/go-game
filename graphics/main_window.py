import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._game_type_buttons = list()
        self._choose_color_buttons = list()
        self.setupUi(self)
        self.retranslateUi(self)
        self.show()

    def setupUi(self, MainWindow):
        MainWindow.setFixedSize(480, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(10, 10, 461, 601)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        # title
        self.title = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        self.title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.title)
        # subtitle
        self.subtitile = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.subtitile.setFont(font)
        self.subtitile.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.subtitile)
        # game_type_layout
        self.game_type_layout = QtWidgets.QHBoxLayout()
        self.online_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        # online_button
        self.online_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.game_type_layout.addWidget(self.online_button)
        self.online_button.setFont(font)
        # local_button
        self.local_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        self._game_type_buttons.append(self.online_button)
        self.local_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.local_button.setFont(font)
        self.game_type_layout.addWidget(self.local_button)
        self._game_type_buttons.append(self.local_button)
        # ai_button
        self.ai_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        self.ai_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.ai_button.setFont(font)
        self.game_type_layout.addWidget(self.ai_button)
        self._game_type_buttons.append(self.ai_button)
        # choose_color_label
        self.verticalLayout.addLayout(self.game_type_layout)
        self.choose_color_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_color_label.sizePolicy()
                                     .hasHeightForWidth())
        self.choose_color_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(14)
        self.choose_color_label.setFont(font)
        self.choose_color_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.choose_color_label)
        # choose_color_layout
        self.choose_color_layout = QtWidgets.QHBoxLayout()
        # white_button
        self.white_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        self.white_button.setSizePolicy(sizePolicy)
        self.white_button.setIcon(QIcon('white.png'))
        self.white_button.setIconSize(QtCore.QSize(80, 80))
        self.choose_color_layout.addWidget(self.white_button)
        self._choose_color_buttons.append(self.white_button)
        # black_button
        self.black_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        self.black_button.setSizePolicy(sizePolicy)
        self.black_button.setIcon(QIcon('black.png'))
        self.black_button.setIconSize(QtCore.QSize(80, 80))
        self.choose_color_layout.addWidget(self.black_button)
        self._choose_color_buttons.append(self.black_button)
        # vertical_layout
        self.verticalLayout.addLayout(self.choose_color_layout)
        # ext_label
        self.ext_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        self.ext_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(14)
        self.ext_label.setFont(font)
        self.ext_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.ext_label)
        # ext_layout
        self.ext_layout = QtWidgets.QGridLayout()
        # field_size_label
        self.field_size_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.field_size_label.setFont(font)
        self.ext_layout.addWidget(self.field_size_label, 0, 0, 1, 1)
        # field_size_spin
        self.field_size_spin = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.field_size_spin.setFont(font)
        self.field_size_spin.setMinimum(1)
        self.field_size_spin.setMaximum(19)
        self.field_size_spin.setProperty("value", 9)
        self.ext_layout.addWidget(self.field_size_spin, 1, 0, 1, 1)
        # time_game_check
        self.time_game_check = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.time_game_check.setFont(font)
        self.ext_layout.addWidget(self.time_game_check, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.ext_layout)
        # start_button
        self.start_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        self.start_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.start_button.setFont(font)
        self.verticalLayout.addWidget(self.start_button)
        MainWindow.setCentralWidget(self.centralwidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "Go"))
        self.subtitile.setText(_translate("MainWindow", "Настройки"))
        self.online_button.setText(_translate("MainWindow", "Онлайн"))
        self.local_button.setText(_translate("MainWindow", "Локально"))
        self.ai_button.setText(_translate("MainWindow", "AI"))
        self.choose_color_label.setText(_translate("MainWindow", "Цвет"))
        self.ext_label.setText(_translate("MainWindow",
                                          "Дополнительные настройки"))
        self.field_size_label.setText(_translate("MainWindow", "Размер поля"))
        self.time_game_check.setText(_translate("MainWindow",
                                                "Игра на время"))
        self.start_button.setText(_translate("MainWindow", "Играть"))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
