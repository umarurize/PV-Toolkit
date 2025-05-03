from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from GUI.window_scale import get_scale_factor


# SubWindow5CurvePreviewForm
class SubWindow5CurvePreviewForm(QWidget):
    def __init__(self, sub_window5: QWidget):
        super().__init__()
        self.sub_window5 = sub_window5
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(450 * get_scale_factor())
        )

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.result = QLabel('', self)
        self.result.setWordWrap(True)

        self.preview = QLabel(self)
        self.preview.hide()

        button = QPushButton('Back', self)
        button.clicked.connect(self.back)

        layout.addWidget(self.result)
        layout.addWidget(self.preview)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319 - Steady Current Helper')

    def back(self):
        pos = self.pos()
        self.hide()
        self.preview.hide()
        self.sub_window5.reset_layout()
        self.sub_window5.move(pos)
        self.sub_window5.show()
