import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDropEvent, QDragEnterEvent, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QTableWidgetItem, QLineEdit, QScrollArea

from GUI.window_scale import get_scale_factor

from GUI.sub_window2.sub_window21_progress_form import SubWindow21ProgressForm


from Functions.iv_helper_two import data_process_two


# SubWindow21 - 1428 Output report
class SubWindow21(QWidget):
    def __init__(self, sub_window2: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.sub_window2 = sub_window2
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(300 * get_scale_factor())
        )
        self.setAcceptDrops(True)

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

        self.prompt_label = QLabel(
            '> Please drag the target folder here...\n'
            '> Only .txt files are accepted...',
            self
        )

        self.path_label = QLabel('', self)
        self.path_label.setWordWrap(True)
        self.path_label.hide()

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText('Please input device area...')
        self.text_input.hide()

        self.button1 = QPushButton('Process', self)
        self.button1.clicked.connect(self.check)
        self.button1.hide()

        self.button2 = QPushButton('Back', self)
        self.button2.clicked.connect(self.back)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.path_label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('1428 - Output report')

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                path = url.toLocalFile()
                if os.path.isdir(path):
                    file_list = os.listdir(path)
                    type_check = []
                    for file in file_list:
                        index = file.rfind('.')
                        if file[index+1:] == 'txt':
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
        self.text_input.show()
        self.button1.show()
        event.accept()

    def reset_layout(self):
        self.prompt_label.setText(
            '> Please drag the target folder here...\n'
            '> Only .txt files are accepted...'
        )
        self.path_label.hide()
        self.text_input.hide()
        self.text_input.setText('')
        self.button1.hide()

    def back(self):
        pos = self.pos()
        self.hide()
        self.reset_layout()
        self.sub_window2.move(pos)
        self.sub_window2.show()

    def check(self):
        try:
            if (
                    isinstance(eval(self.text_input.text()), int)
                    or
                    isinstance(eval(self.text_input.text()), float)
            ):
                self.process()
            else:
                self.text_input.setText('')
        except:
            self.text_input.setText('')

    def process(self):
        pos = self.pos()
        self.hide()
        self.sub_window21_progress_form = SubWindow21ProgressForm(self)
        self.sub_window21_progress_form.move(pos)
        self.sub_window21_progress_form.show()

        path = self.path_label.text().split('\n')[1]

        area = self.text_input.text()

        total_steps = 100
        self.sub_window21_progress_form.result_intime_box_text.show()
        for data_intime in data_process_two(path, area):
            QApplication.processEvents()

            self.sub_window21_progress_form.set_progress(data_intime[1], total_steps)

            result_intime = [str(i) for i in data_intime[0]]

            row_count = self.sub_window21_progress_form.result_intime_sheet.rowCount()
            self.sub_window21_progress_form.result_intime_sheet.insertRow(row_count)
            self.sub_window21_progress_form.result_intime_sheet.setRowHeight(row_count, int(25 * get_scale_factor()))
            for col in range(9):
                item = QTableWidgetItem(result_intime[col])
                self.sub_window21_progress_form.result_intime_sheet.setItem(
                    row_count,
                    col,
                    item
                )

        self.sub_window21_progress_form.progress_bar_label.setText(
            '> All done!\n'
            '> Report workbook has been saved to the source folder...'
        )

        self.sub_window21_progress_form.button.show()