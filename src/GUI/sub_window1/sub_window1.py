from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea

from GUI.window_scale import get_scale_factor

from GUI.sub_window1.sub_window11 import SubWindow11
from GUI.sub_window1.sub_window12 import SubWindow12
from GUI.sub_window1.sub_window13 import SubWindow13


# SubWindow1 - 319 IV Helper
class SubWindow1(QWidget):
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

        prompt_label = QLabel('Please select a function...')

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

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
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