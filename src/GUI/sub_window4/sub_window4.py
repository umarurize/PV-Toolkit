import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from GUI.window_scale import get_scale_factor

from GUI.sub_window4.sub_window4_curve_preview_form import SubWindow4CurvePreviewForm

from Functions.eqe_helper import curve_preview_four


# SubWindow4 - 317 EQE Helper
class SubWindow4(QWidget):
    def __init__(self, main_window: QWidget):
        super().__init__()
        self.main_window = main_window
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
        self.path_label.setWordWrap(True)
        self.path_label.hide()

        self.button1 = QPushButton('Preview', self)
        self.button1.clicked.connect(self.process)
        self.button1.hide()

        button2 = QPushButton('Back', self)
        button2.clicked.connect(self.back)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.path_label)
        layout.addWidget(self.button1)
        layout.addWidget(button2)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('317 - EQE Helper')

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
        self.prompt_label.setText('> Ready for previwing...')
        self.path_label.setText(f'> File path\n{path}')
        self.path_label.show()
        self.button1.show()
        event.accept()

    def reset_layout(self):
        self.prompt_label.setText(
            '> Please drag the target file here...\n'
            '> Only .txt file is accepted...',
        )
        self.path_label.hide()
        self.button1.hide()

    def back(self):
        pos = self.pos()
        self.hide()
        self.reset_layout()
        self.main_window.move(pos)
        self.main_window.show()

    def process(self):
        pos = self.pos()
        self.hide()

        self.sub_window4_curve_preview_form = SubWindow4CurvePreviewForm(self)

        path = self.path_label.text().split('\n')[1]

        data_intime = curve_preview_four(path)

        img_bytes = data_intime[-1].read()

        img = QImage()
        img.loadFromData(img_bytes)

        pixmap = QPixmap.fromImage(img)
        width = int(400 * get_scale_factor())
        height = int(300 * get_scale_factor())
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)

        result_text = '> Result\n'
        result_text += f'Name: {data_intime[0]}\n'
        result_text += f'Cal.Jsc: {data_intime[1]}'

        self.sub_window4_curve_preview_form.result.setText(result_text)

        self.sub_window4_curve_preview_form.preview.setPixmap(pixmap)
        self.sub_window4_curve_preview_form.preview.show()
        self.sub_window4_curve_preview_form.button1.show()

        self.sub_window4_curve_preview_form.move(pos)
        self.sub_window4_curve_preview_form.show()
