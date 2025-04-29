from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from GUI.sub_window3.sub_window31 import SubWindow31
from GUI.sub_window3.sub_window32 import SubWindow32
from GUI.sub_window3.sub_window33 import SubWindow33


# SubWindow3 - 319[1] IV Helper
class SubWindow3(QWidget):
    def __init__(self, main_window: QWidget):
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

        button1 = QPushButton('Output report', self)
        button1.clicked.connect(self.open_sub_window31)

        button2 = QPushButton('Preview and transfer J-V curve', self)
        button2.clicked.connect(self.open_sub_window32)

        button3 = QPushButton('Reload configurations', self)
        button3.clicked.connect(self.open_sub_window33)

        button4 =QPushButton('Back', self)
        button4.clicked.connect(self.back)

        layout.addWidget(prompt_label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319[1] - IV Helper')

        self.sub_window31 = SubWindow31(self)
        self.sub_window32 = SubWindow32(self)
        self.sub_window33 = SubWindow33(self)

    def back(self):
        pos = self.pos()
        self.hide()
        self.main_window.move(pos)
        self.main_window.show()

    def open_sub_window31(self):
        pos = self.pos()
        self.hide()
        self.sub_window31.move(pos)
        self.sub_window31.show()

    def open_sub_window32(self):
        pos = self.pos()
        self.hide()
        self.sub_window32.move(pos)
        self.sub_window32.show()

    def open_sub_window33(self):
        pos = self.pos()
        self.hide()
        self.sub_window33.move(pos)
        self.sub_window33.show()

