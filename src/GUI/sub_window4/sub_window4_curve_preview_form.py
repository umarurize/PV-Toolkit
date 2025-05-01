from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from GUI.window_scale import get_scale_factor


# SubWindow4CurvePreviewForm
class SubWindow4CurvePreviewForm(QWidget):
    def __init__(self, sub_window4: QWidget):
        super().__init__()
        self.sub_window4 = sub_window4
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(400 * get_scale_factor())
        )

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.result = QLabel('', self)

        self.preview = QLabel(self)
        self.preview.hide()

        self.button1 = QPushButton('Transfer', self)
        self.button1.clicked.connect(self.transfer)
        self.button1.hide()

        self.transfer_message = QLabel('Successfully transfered...', self)
        self.transfer_message.hide()

        button2 = QPushButton('Back', self)
        button2.clicked.connect(self.back)


        layout.addWidget(self.result)
        layout.addWidget(self.preview)
        layout.addWidget(self.button1)
        layout.addWidget(self.transfer_message)
        layout.addWidget(button2)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('317 - EQE Helper')

    def transfer(self):
        pass

    def back(self):
        pos = self.pos()
        self.hide()
        self.preview.hide()
        self.transfer_message.hide()
        self.sub_window4.reset_layout()
        self.sub_window4.move(pos)
        self.sub_window4.show()
