from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea

from GUI.window_scale import get_scale_factor


# SubWindow5CurvePreviewForm
class SubWindow5CurvePreviewForm(QWidget):
    def __init__(self, sub_window5: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.sub_window5 = sub_window5
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(450 * get_scale_factor())
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
        self.result.setWordWrap(True)

        self.preview = QLabel(self)
        self.preview.hide()

        button = QPushButton('Back', self)
        button.clicked.connect(self.back)

        layout.addWidget(self.result)
        layout.addWidget(self.preview)
        layout.addWidget(button)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('319 - Steady Current Helper')

    def back(self):
        pos = self.pos()
        self.hide()
        self.preview.hide()
        self.sub_window5.reset_layout()
        self.sub_window5.move(pos)
        self.sub_window5.show()
