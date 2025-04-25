from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget

from Functions.iv_curve_preview_two import type_transfer


# SubWindow22CurvePreviewForm
class Subwindow22CurvePreviewForm(QWidget):
    def __init__(self, sub_window22):
        super().__init__()
        self.sub_window22 = sub_window22
        self.initUI()
        self.setFixedSize(400, 550)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.result = QLabel('', self)

        self.result_sheet = QTableWidget(self)
        self.result_sheet.setRowCount(0)
        self.result_sheet.setColumnCount(5)
        for i in range(5):
            self.result_sheet.setColumnWidth(i, 70)
        headers = ['Mode','Voc', 'Jsc', 'FF', 'PCE']
        self.result_sheet.setHorizontalHeaderLabels(headers)
        self.result_sheet.hide()

        self.preview = QLabel(self)

        self.button1 = QPushButton('Transfer', self)
        self.button1.clicked.connect(self.transfer)
        self.button1.hide()

        self.transfer_message = QLabel('Successfully transfered...', self)
        self.transfer_message.hide()

        button2 = QPushButton('Back', self)
        button2.clicked.connect(self.back)

        layout.addWidget(self.result)
        layout.addWidget(self.result_sheet)
        layout.addWidget(self.preview)
        layout.addWidget(self.button1)
        layout.addWidget(self.transfer_message)
        layout.addWidget(button2)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('1428 - Preview and transfer J-V curve')

    def transfer(self):
        path = self.sub_window22.path_label.text().split('\n')[1]
        type_transfer(path)
        self.button1.hide()
        self.transfer_message.show()

    def back(self):
        pos = self.pos()
        self.hide()
        self.button1.hide()
        self.transfer_message.hide()
        self.sub_window22.reset_layout()
        self.sub_window22.move(pos)
        self.sub_window22.show()