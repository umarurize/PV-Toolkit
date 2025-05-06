from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea

from GUI.window_scale import get_scale_factor

from GUI.sub_window2.sub_window21 import SubWindow21
from GUI.sub_window2.sub_window22 import SubWindow22


# SubWindow2 - 1428 IV Helper
class SubWindow2(QWidget):
    def __init__(self, main_window: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.main_window = main_window
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(300 * get_scale_factor())
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

        prompt_label = QLabel('Please select a function...', self)

        button1 = QPushButton('Output report', self)
        button1.clicked.connect(self.open_sub_window21)

        button2 = QPushButton('Preview and converse J-V curve', self)
        button2.clicked.connect(self.open_sub_window22)

        button3 = QPushButton('Back', self)
        button3.clicked.connect(self.back)

        layout.addWidget(prompt_label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('1428 - IV Helper')

        self.sub_window21 = SubWindow21(self)
        self.sub_window22 = SubWindow22(self)

    def open_sub_window21(self):
        pos = self.pos()
        self.hide()
        self.sub_window21.move(pos)
        self.sub_window21.show()

    def open_sub_window22(self):
        pos = self.pos()
        self.hide()
        self.sub_window22.move(pos)
        self.sub_window22.show()

    def back(self):
        pos = self.pos()
        self.hide()
        self.main_window.move(pos)
        self.main_window.show()