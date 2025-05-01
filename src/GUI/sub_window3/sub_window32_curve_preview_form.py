from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from GUI.window_scale import get_scale_factor

from Functions.iv_curve_preview_three import type_converse_two


# SubWindow32CurvePreviewForm
class SubWindow32CurvePreviewForm(QWidget):
    def __init__(self, sub_window32: QWidget):
        super().__init__()
        self.sub_window32 = sub_window32
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(480 * get_scale_factor())
        )
    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.result = QLabel('', self)

        self.preview = QLabel(self)
        self.preview.hide()

        self.button1 = QPushButton('Converse', self)
        self.button1.clicked.connect(self.converse)
        self.button1.hide()

        self.converse_message = QLabel('Successfully conversed...', self)
        self.converse_message.hide()

        button2 = QPushButton('Back', self)
        button2.clicked.connect(self.back)

        layout.addWidget(self.result)
        layout.addWidget(self.preview)
        layout.addWidget(self.button1)
        layout.addWidget(self.converse_message)
        layout.addWidget(button2)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319[1] - Preview and tranfer J-V curve')

    def converse(self):
        path = self.sub_window32.path_label.text().split('\n')[1]
        area = self.sub_window32.text_input.text()
        type_converse_two(path, area)
        self.button1.hide()
        self.converse_message.show()

    def back(self):
        pos = self.pos()
        self.hide()
        self.preview.hide()
        self.button1.hide()
        self.converse_message.hide()
        self.sub_window32.reset_layout()
        self.sub_window32.move(pos)
        self.sub_window32.show()