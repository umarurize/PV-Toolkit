from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


# Subwindow12CurvePreviewForm
class Subwindow12CurvePreviewForm(QWidget):
    def __init__(self, sub_window12):
        super().__init__()
        self.sub_window12 = sub_window12
        self.initUI()
        self.setFixedSize(400, 450)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.result = QLabel('', self)

        self.preview = QLabel(self)

        self.transfer_button = QPushButton('Transfer')
        self.transfer_button.hide()

        button = QPushButton('Back', self)
        button.clicked.connect(self.back)

        layout.addWidget(self.result)
        layout.addWidget(self.preview)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319 - Preview J-V curve')

    def transfer(self):
        pass

    def back(self):
        pos = self.pos()
        self.hide()
        self.sub_window12.move(pos)
        self.sub_window12.show()