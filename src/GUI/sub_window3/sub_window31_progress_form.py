from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTableWidget

from GUI.window_scale import get_scale_factor


# SubWindow31ProgressForm
class SubWindow31ProgressForm(QWidget):
    def __init__(self, sub_window31: QWidget):
        super().__init__()
        self.sub_window31 = sub_window31
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(300 * get_scale_factor())
        )

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.progress_bar_label = QLabel('> Processing...', self)

        self.progress_bar = QProgressBar(self)

        self.result_intime_box_text = QLabel('> Result intime', self)
        self.result_intime_box_text.hide()

        self.result_intime_sheet = QTableWidget(self)
        self.result_intime_sheet.setRowCount(0)
        self.result_intime_sheet.setColumnCount(5)
        for i in range(5):
            self.result_intime_sheet.setColumnWidth(i, int(65 * get_scale_factor()))
        headers = ['Name', 'Voc', 'Jsc', 'FF', 'PCE']
        self.result_intime_sheet.setHorizontalHeaderLabels(headers)

        self.result_message = QLabel('')
        self.result_message.setWordWrap(True)
        self.result_message.hide()

        self.button = QPushButton('Back', self)
        self.button.clicked.connect(self.back)
        self.button.hide()

        layout.addWidget(self.progress_bar_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_intime_box_text)
        layout.addWidget(self.result_intime_sheet)
        layout.addWidget(self.result_message)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319[1] - Output report')

    def set_progress(self, value, total):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(value)

    def back(self):
        pos = self.pos()
        self.hide()
        self.sub_window31.reset_layout()
        self.sub_window31.move(pos)
        self.sub_window31.show()
