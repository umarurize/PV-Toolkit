import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDropEvent, QDragEnterEvent, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QTableWidgetItem

from GUI.sub_window1.sub_window11_progress_form import SubWindow11ProgressForm

from Functions.iv_helper import data_process


# SubWindow11 - 319 Output report
class SubWindow11(QWidget):
    def __init__(self, sub_window1):
        super().__init__()
        self.subwindow1 = sub_window1
        self.initUI()
        self.setFixedSize(400, 300)
        self.setAcceptDrops(True)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.prompt_label = QLabel(
            '> Please drag the target folder here...\n'
            '> Only .txt files are accepted...',
            self
        )

        self.path_label = QLabel('', self)
        self.path_label.hide()

        self.button1 = QPushButton('Process', self)
        self.button1.clicked.connect(self.process)
        self.button1.hide()

        self.button2 = QPushButton('Back', self)
        self.button2.clicked.connect(self.back)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.path_label)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319 - Output report')

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                path = url.toLocalFile()
                if os.path.isdir(path):
                    file_list = os.listdir(path)
                    type_check = []
                    for file in file_list:
                        if file.split('.')[1] == 'txt':
                            type_check.append(True)
                        else:
                            type_check.append(False)
                    if all(type_check):
                        event.accept()
                        return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        url = event.mimeData().urls()[0]
        path = url.toLocalFile()
        self.prompt_label.setText('> Ready for processing...')
        self.path_label.setText(f'> Folder path\n{path}')
        self.path_label.show()
        self.button1.show()
        event.accept()

    def reset_layout(self):
        self.prompt_label.setText(
            '> Please drag the target folder here...\n'
            '> Only .txt files are accepted...'
        )
        self.path_label.hide()
        self.button1.hide()

    def back(self):
        pos = self.pos()
        self.hide()
        self.reset_layout()
        self.subwindow1.move(pos)
        self.subwindow1.show()

    def process(self):
        pos = self.pos()
        self.hide()
        self.reset_layout()
        self.sub_window11_progress_form = SubWindow11ProgressForm(self)
        self.sub_window11_progress_form.move(pos)
        self.sub_window11_progress_form.show()

        path = self.path_label.text().split('\n')[1]
        total_steps = 100
        self.sub_window11_progress_form.result_intime_box_text.show()
        for data_intime in data_process(path):
            QApplication.processEvents()

            self.sub_window11_progress_form.set_progress(data_intime[1], total_steps)

            result_intime = [str(i) for i in data_intime[0]]

            row_count = self.sub_window11_progress_form.result_intime_sheet.rowCount()
            self.sub_window11_progress_form.result_intime_sheet.insertRow(row_count)
            for col in range(5):
                item = QTableWidgetItem(result_intime[col])
                self.sub_window11_progress_form.result_intime_sheet.setItem(
                    row_count,
                    col,
                    item
                )

        self.sub_window11_progress_form.progress_bar_label.setText('> Done!')
        self.sub_window11_progress_form.result_message.setText(
            'Report workbook has been saved to the source folder...'
        )
        self.sub_window11_progress_form.result_message.show()
        self.sub_window11_progress_form.button.show()