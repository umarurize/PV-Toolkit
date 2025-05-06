from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTableWidget, QScrollArea

from GUI.window_scale import get_scale_factor


# SubWindow21ProgressForm
class SubWindow21ProgressForm(QWidget):
    def __init__(self, sub_window21: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.sub_window21 = sub_window21
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

        self.progress_bar_label = QLabel('> Processing...', self)
        self.progress_bar_label.setWordWrap(True)

        self.progress_bar = QProgressBar(self)

        self.result_intime_box_text = QLabel('> Result intime', self)
        self.result_intime_box_text.hide()

        self.result_intime_sheet = QTableWidget(self)
        self.result_intime_sheet.setRowCount(0)
        self.result_intime_sheet.setColumnCount(9)
        for i in range(9):
            self.result_intime_sheet.setColumnWidth(i, int(60 * get_scale_factor()))
        headers = ['Name', 'Voc_1', 'Jsc_1', 'FF_1', 'PCE_1',
                   'Voc_2', 'Jsc_2', 'FF_2', 'PCE_2']
        self.result_intime_sheet.setHorizontalHeaderLabels(headers)

        self.button = QPushButton('Back', self)
        self.button.clicked.connect(self.back)
        self.button.hide()

        layout.addWidget(self.progress_bar_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_intime_box_text)
        layout.addWidget(self.result_intime_sheet)
        layout.addWidget(self.button)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('1428 - Output report')

    def set_progress(self, value, total):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(value)

    def back(self):
        pos = self.pos()
        self.hide()
        self.sub_window21.reset_layout()
        self.sub_window21.move(pos)
        self.sub_window21.show()
