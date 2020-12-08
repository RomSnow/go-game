import PyQt5.QtWidgets as qtw

from game_core.board_managers import BoardManager


class ScoreBoardWindow(qtw.QWidget):
    def __init__(self, board_manager: BoardManager, main_window):
        super().__init__()
        self._board = board_manager
        self._init_ui()
        self.show()
        self.main_window = main_window
        main_window.hide()

    def _init_ui(self):
        self.setFixedSize(480, 600)
        self.setWindowTitle(self._board.get_board_name())

        main_label = qtw.QVBoxLayout()
        text_label = qtw.QLabel()
        scroll_area = qtw.QScrollArea()

        text_label.setText(self._board.get_board_str())
        text_label.setSizePolicy(qtw.QSizePolicy.Preferred,
                                 qtw.QSizePolicy.Preferred)
        scroll_area.setWidget(text_label)

        ok_button = qtw.QPushButton('Закрыть')
        ok_button.clicked.connect(self.close)

        main_label.addWidget(scroll_area)
        main_label.addWidget(ok_button)

        self.setLayout(main_label)

    def closeEvent(self, a0):
        self.main_window.show()
