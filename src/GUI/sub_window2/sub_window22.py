import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidgetItem

from GUI.window_scale import get_scale_factor

from GUI.sub_window2.sub_window22_curve_preview_form import Subwindow22CurvePreviewForm

from Functions.iv_curve_preview_two import curve_preview_two


# SubWindow22 - 1428 Preview and transfer J-V curve
class SubWindow22(QWidget):
    def __init__(self, sub_window2: QWidget):
        super().__init__()
        self.sub_window2 = sub_window2
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(300 * get_scale_factor())
        )
        self.setAcceptDrops(True)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.prompt_label = QLabel(
            '> Please drag the target file here...\n'
            '> Only .txt file is accepted...',
            self
        )

        self.path_label = QLabel('', self)
        self.path_label.hide()

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText('Please input device area...')
        self.text_input.hide()

        self.button1 = QPushButton('Preview', self)
        self.button1.clicked.connect(self.check)
        self.button1.hide()

        button2 = QPushButton('Back', self)
        button2.clicked.connect(self.back)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.path_label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.button1)
        layout.addWidget(button2)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('1428 - Preview and transfer J-V curve')

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    index = path.rfind('.')
                    if path[index+1:] == 'txt':
                        event.accept()
                        return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        url = event.mimeData().urls()[0]
        path = url.toLocalFile()
        self.prompt_label.setText('> Ready for previewing...')
        self.path_label.setText(f'> File path\n{path}')
        self.path_label.show()
        self.text_input.show()
        self.button1.show()
        event.accept()

    def reset_layout(self):
        self.prompt_label.setText(
            '> Please drag the target file here...\n'
            '> Only .txt file is accepted...'
        )
        self.path_label.hide()
        self.text_input.hide()
        # Remember the last device area input
        '''self.text_input.setText('')'''
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

        self.sub_window22_curve_preview_form = Subwindow22CurvePreviewForm(self)

        path = self.path_label.text().split('\n')[1]

        area = self.text_input.text()

        data_in_time = curve_preview_two(path, area)

        if len(data_in_time) == 2:
            result_text = ('> Result\n'
                           'Whoops! It is a bad data...')
            self.sub_window22_curve_preview_form.result.setText(result_text)
        else:
            result_text = ('> Result\n'
                           f'Name: {data_in_time[0]}\n'
                           f'Area: {data_in_time[1]}\n')
            HI = str(round((data_in_time[5] - data_in_time[9]) / data_in_time[5], 4))
            result_text += f'HI: {HI}'

            for i in range(2):
                row_count = self.sub_window22_curve_preview_form.result_sheet.rowCount()
                self.sub_window22_curve_preview_form.result_sheet.insertRow(row_count)
                self.sub_window22_curve_preview_form.result_sheet.setRowHeight(row_count, int(25 * get_scale_factor()))
                if i == 0:
                    result = ['Reverse'] + [str(i) for i in data_in_time[2:6]]
                else:
                    result = ['Forward'] + [str(i) for i in data_in_time[6:10]]
                for col in range(5):
                    item = QTableWidgetItem(result[col])
                    self.sub_window22_curve_preview_form.result_sheet.setItem(
                        row_count,
                        col,
                        item
                    )

            img_bytes = data_in_time[-1].read()

            img = QImage()
            img.loadFromData(img_bytes)

            pixmap = QPixmap.fromImage(img)
            scale_factor = get_scale_factor()
            width = int(400 * scale_factor)
            height = int(300 * scale_factor)
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)

            self.sub_window22_curve_preview_form.result.setText(result_text)
            self.sub_window22_curve_preview_form.result_sheet.show()
            self.sub_window22_curve_preview_form.preview.setPixmap(pixmap)
            self.sub_window22_curve_preview_form.preview.show()
            self.sub_window22_curve_preview_form.button1.show()

        self.sub_window22_curve_preview_form.move(pos)
        self.sub_window22_curve_preview_form.show()