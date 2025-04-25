from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from GUI.sub_window1.sub_window11 import SubWindow11
from GUI.sub_window1.sub_window12 import SubWindow12
from GUI.sub_window1.sub_window13 import SubWindow13


# SubWindow1 - 319 IV Helper
class SubWindow1(QWidget):
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

        prompt_label = QLabel('Please select a function...')
        prompt_label.setFixedSize(300, 10)

        button_1 = QPushButton('Output report', self)
        button_1.clicked.connect(self.open_sub_window11)

        button_2 = QPushButton('Preview J-V curve', self)
        button_2.clicked.connect(self.open_sub_window12)

        button_3 = QPushButton('Reload configurations', self)
        button_3.clicked.connect(self.open_sub_window13)


        button_4 = QPushButton('Back', self)
        button_4.clicked.connect(self.back)

        layout.addWidget(prompt_label)
        layout.addWidget(button_1)
        layout.addWidget(button_2)
        layout.addWidget(button_3)
        layout.addWidget(button_4)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319 - IV Helper')

        self.sub_window11 = SubWindow11(self)
        self.sub_window12 = SubWindow12(self)
        self.sub_window13 = SubWindow13(self)

    def open_sub_window11(self):
        pos = self.pos()
        self.hide()
        self.sub_window11.move(pos)
        self.sub_window11.show()

    def open_sub_window12(self):
        pos = self.pos()
        self.hide()
        self.sub_window12.move(pos)
        self.sub_window12.show()

    def open_sub_window13(self):
        pos = self.pos()
        self.hide()
        self.sub_window13.move(pos)
        self.sub_window13.show()

    def back(self):
        pos = self.pos()
        self.hide()
        self.main_window.move(pos)
        self.main_window.show()