from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class WaitWindow(QWidget):

    def __init__(self):
        super().__init__()
        self._set_ui()
        self.show()

    def _set_ui(self):
        main_layout = QHBoxLayout()
        text = QLabel('Ожидание другого игрока...')
        main_layout.addWidget(text)
        self.setLayout(main_layout)
