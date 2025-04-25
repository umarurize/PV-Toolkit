from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from GUI.sub_window2.sub_window21 import SubWindow21
from GUI.sub_window2.sub_window22 import SubWindow22


# SubWindow2 - 1428 IV Helper
class SubWindow2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.setFixedSize(400, 300)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        prompt_label = QLabel('Please select a function...', self)

        button1 = QPushButton('Output report', self)
        button1.clicked.connect(self.open_sub_window21)

        button2 = QPushButton('Preview and transfer J-V curve', self)
        button2.clicked.connect(self.open_sub_window22)

        button3 = QPushButton('Back', self)
        button3.clicked.connect(self.back)

        layout.addWidget(prompt_label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('1428 - IV Helper')

        self.sub_window_21 = SubWindow21(self)
        self.sub_window_22 = SubWindow22(self)

    def open_sub_window21(self):
        pos = self.pos()
        self.hide()
        self.sub_window_21.move(pos)
        self.sub_window_21.show()

    def open_sub_window22(self):
        pos = self.pos()
        self.hide()
        self.sub_window_22.move(pos)
        self.sub_window_22.show()

    def back(self):
        pos = self.pos()
        self.hide()
        self.main_window.move(pos)
        self.main_window.show()