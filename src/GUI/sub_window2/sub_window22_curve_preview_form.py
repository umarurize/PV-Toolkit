from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea

from GUI.window_scale import get_scale_factor

from Functions.iv_curve_preview_two import type_converse


# SubWindow22CurvePreviewForm
class Subwindow22CurvePreviewForm(QWidget):
    def __init__(self, sub_window22: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.sub_window22 = sub_window22
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(520 * get_scale_factor())
        )

    def initUI(self):
        main_layout = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        function_widget = QWidget()
        layout = QVBoxLayout(function_widget)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(int(10 * get_scale_factor()))

        icon = QIcon('resources/logo.ico')

        font = QFont()
        font_size = int(8 * get_scale_factor())
        font.setPointSize(font_size)
        font.setFamily('Microsoft YaHei')

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

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('1428 - Preview and converse J-V curve')

    def converse(self):
        path = self.sub_window22.path_label.text().split('\n')[1]
        area = self.sub_window22.text_input.text()
        type_converse(path, area)
        self.button1.hide()
        self.converse_message.show()

    def back(self):
        pos = self.pos()
        self.hide()
        self.preview.hide()
        self.button1.hide()
        self.converse_message.hide()
        self.sub_window22.reset_layout()
        self.sub_window22.move(pos)
        self.sub_window22.show()
