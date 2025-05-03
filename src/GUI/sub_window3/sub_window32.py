import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit

from GUI.window_scale import get_scale_factor

from GUI.sub_window3.sub_window32_curve_preview_form import SubWindow32CurvePreviewForm

from Functions.iv_curve_preview_three import curve_preview_three


# SubWindow32 - 319[1] Preview and converse J-V curve
class SubWindow32(QWidget):
    def __init__(self, sub_window3: QWidget):
        super().__init__()
        self.sub_window3 = sub_window3
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
            '> Only .csv file is accepted...',
            self
        )

        self.path_label = QLabel('', self)
        self.path_label.setWordWrap(True)
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
        self.setWindowTitle('319[1] - Preview and converse J-V curve')

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    index = path.rfind('.')
                    if path[index+1:] == 'csv':
                        event.accept()
                        return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        url = event.mimeData().urls()[0]
        path = url.toLocalFile()
        self.prompt_label.setText('> Ready for previwing...')
        self.path_label.setText(f'> File path\n{path}')
        self.path_label.show()
        self.text_input.show()
        self.button1.show()
        event.accept()

    def reset_layout(self):
        self.prompt_label.setText(
            '> Please drag the target file here...\n'
            '> Only .csv file is accepted...',
        )
        self.path_label.hide()
        self.text_input.hide()
        self.button1.hide()

    def back(self):
        pos = self.pos()
        self.hide()
        self.reset_layout()
        self.sub_window3.move(pos)
        self.sub_window3.show()

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

        self.sub_window32_curve_preview_form = SubWindow32CurvePreviewForm(self)

        path = self.path_label.text().split('\n')[1]

        area = self.text_input.text()

        data_intime = curve_preview_three(path, area)

        if len(data_intime) == 2:
            result_text = ('> Result\n'
                           'Whoops! It is a bad data...')
            self.sub_window32_curve_preview_form.result.setText(result_text)
        else:
            img_bytes = data_intime[-1].read()

            img = QImage()
            img.loadFromData(img_bytes)

            pixmap = QPixmap.fromImage(img)
            width = int(400 * get_scale_factor())
            height = int(300 * get_scale_factor())
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)

            result_text = '> Result\n'
            result_text += f'Name: {data_intime[0]}\n'
            result_text += f'Area: {data_intime[1]}\n'
            result_text += f'Voc: {data_intime[2]}\n'
            result_text += f'Jsc: {data_intime[3]}\n'
            result_text += f'FF: {data_intime[4]}\n'
            result_text += f'PCE: {data_intime[5]}\n'
            result_text += f'Mode: {data_intime[6]}'

            self.sub_window32_curve_preview_form.result.setText(result_text)
            self.sub_window32_curve_preview_form.preview.setPixmap(pixmap)

            self.sub_window32_curve_preview_form.preview.show()
            self.sub_window32_curve_preview_form.button1.show()

        self.sub_window32_curve_preview_form.move(pos)
        self.sub_window32_curve_preview_form.show()







