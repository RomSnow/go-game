import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

import graphics.game_window as game_win
from game_core.game_modes import GameModes
from web.guest_room import GuestRoom
from web.host_room import HostRoom


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._game_type_buttons = list()
        self._choose_color_buttons = list()
        self._game_mode = game_win.gm.GameModes.local
        self._main_player = 'white'
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
        # online_button
        self.online_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        self.online_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.game_type_layout.addWidget(self.online_button)
        self.online_button.setFont(font)
        self.online_button.game_type = game_win.gm.GameModes.online
        self.online_button.clicked.connect(lambda _t:
                                           self._game_type_buttons_func(
                                               self.online_button
                                           ))
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
        self.local_button.game_type = game_win.gm.GameModes.local
        self.local_button.clicked.connect(lambda _t:
                                          self._game_type_buttons_func(
                                              self.local_button
                                          ))
        # ai_button
        self.ai_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        self.ai_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.ai_button.setFont(font)
        self.game_type_layout.addWidget(self.ai_button)
        self._game_type_buttons.append(self.ai_button)
        self.ai_button.game_type = game_win.gm.GameModes.ai
        self.ai_button.clicked.connect(lambda _t:
                                       self._game_type_buttons_func(
                                           self.ai_button
                                       ))
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        self.white_button.setSizePolicy(sizePolicy)
        self.white_button.setIcon(QIcon('white.png'))
        self.white_button.setIconSize(QtCore.QSize(80, 80))
        self.choose_color_layout.addWidget(self.white_button)
        self._choose_color_buttons.append(self.white_button)
        self.white_button.color = 'white'
        self.white_button.clicked.connect(lambda _t:
                                          self._color_button_func(
                                              self.white_button
                                          ))
        # black_button
        self.black_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Preferred)
        self.black_button.setSizePolicy(sizePolicy)
        self.black_button.setIcon(QIcon('black.png'))
        self.black_button.setIconSize(QtCore.QSize(80, 80))
        self.choose_color_layout.addWidget(self.black_button)
        self._choose_color_buttons.append(self.black_button)
        self.black_button.color = 'black'
        self.black_button.clicked.connect(lambda _t:
                                          self._color_button_func(
                                              self.black_button
                                          ))
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
        self.start_button.clicked.connect(self._play_button_func)
        # create_button
        self.create_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        self.create_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.create_button.setFont(font)
        self.verticalLayout.addWidget(self.create_button)
        self.create_button.clicked.connect(self._create_button_func)
        self.create_button.hide()
        # connect_button
        self.connect_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        self.connect_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.connect_button.setFont(font)
        self.verticalLayout.addWidget(self.connect_button)
        self.connect_button.hide()
        self.connect_button.clicked.connect(self._connect_button_func)
        MainWindow.setCentralWidget(self.centralwidget)
        # record_button
        self.record_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        self.record_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.record_button.setFont(font)
        self.verticalLayout.addWidget(self.record_button)
        self.record_button.clicked.connect(self._record_button_func)
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
        self.create_button.setText(_translate("MainWindow", "Создать"))
        self.connect_button.setText(_translate("MainWindow", "Подключиться"))
        self.record_button.setText(_translate("MainWindow", "Рекорды"))

    def _play_button_func(self):
        game_params = game_win.gm.GameParams(
            game_mode=self._game_mode,
            field_params=game_win.gm.field.FieldParams(self.field_size_spin.
                                                       value()),
            main_player=self._main_player,
            is_time_mode=self.time_game_check.isChecked()
        )
        game_window = game_win.GameWindow(game_params, self)
        self.hide()

    def _game_type_buttons_func(self, clicked_button):
        self._game_mode = clicked_button.game_type
        if self._game_mode == GameModes.online:
            self.connect_button.show()
            self.create_button.show()
            self.start_button.hide()
            self.record_button.hide()
        else:
            self.connect_button.hide()
            self.create_button.hide()
            self.start_button.show()
            self.record_button.show()
        for button in self._game_type_buttons:
            if button == clicked_button:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Preferred,
                    QtWidgets.QSizePolicy.Preferred))
            else:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Maximum,
                    QtWidgets.QSizePolicy.Preferred))

    def _color_button_func(self, clicked_button):
        self._main_player = clicked_button.color
        for button in self._choose_color_buttons:
            if button == clicked_button:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Preferred,
                    QtWidgets.QSizePolicy.Preferred))

            else:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Maximum,
                    QtWidgets.QSizePolicy.Preferred))

    def _connect_button_func(self):
        address, ok = QtWidgets.QInputDialog.getText(self,
                                                     'Подключение',
                                                     'Введите код игры:')
        if not ok:
            return

        guest_room = GuestRoom(address)
        game_params = guest_room.set_connection()

        game_window = game_win.GameWindow(game_params, self, guest_room)
        self.hide()

    def _create_button_func(self):
        host_room = HostRoom()
        address = host_room.get_address_code()
        try:
            reply = AddressOutMessage(address)
        except ExitException:
            host_room.close()
            return

        game_params = game_win.gm.GameParams(
            game_mode=self._game_mode,
            field_params=game_win.gm.field.FieldParams(self.field_size_spin.
                                                       value()),
            main_player=self._main_player,
            is_time_mode=self.time_game_check.isChecked()
        )

        host_room.wait_connection(game_params)

        game_window = game_win.GameWindow(game_params, self, host_room)
        self.hide()

    def _record_button_func(self):
        pass


class AddressOutMessage(QtWidgets.QMessageBox):
    def __init__(self, address: str):
        super().__init__()
        self.setWindowTitle('Подключение')
        self.setText(f'Код игры: {address}')
        self.setInformativeText('Ожидание подключения')
        ext_button = self.addButton('Отмена',
                                    QtWidgets.QMessageBox.RejectRole)
        self.exec()

        if self.clickedButton() == ext_button:
            raise ExitException


class ExitException(Exception):
    pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
