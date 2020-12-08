import PyQt5.QtWidgets as qtw

from game_core.board_managers import BoardManager


class BoardWindow(qtw.QWidget):
    def __init__(self, board_manager: BoardManager, main_window):
        super().__init__()
        self._board = board_manager
        self.text_label = None
        self._init_ui()
        self.show()
        self.main_window = main_window

    def _init_ui(self):
        self.setFixedSize(480, 600)
        self.setWindowTitle(self._board.get_board_name())

        main_label = qtw.QVBoxLayout()
        self.scroll_area = qtw.QScrollArea()
        self.text_label = qtw.QLabel()

        self.text_label.setText(self._board.get_board_str())
        self.text_label.setSizePolicy(qtw.QSizePolicy.Preferred,
                                      qtw.QSizePolicy.Preferred)
        self.scroll_area.setWidget(self.text_label)

        ok_button = qtw.QPushButton('Закрыть')
        ok_button.clicked.connect(self.close)

        main_label.addWidget(self.scroll_area)
        main_label.addWidget(ok_button)

        self.setLayout(main_label)

    def update_text(self):
        self.text_label.close()
        self.text_label = qtw.QLabel(self._board.get_board_str())
        self.text_label.setSizePolicy(qtw.QSizePolicy.Preferred,
                                      qtw.QSizePolicy.Preferred)
        self.scroll_area.setWidget(self.text_label)
