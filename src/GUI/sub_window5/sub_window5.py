import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QScrollArea

from GUI.window_scale import get_scale_factor

from GUI.sub_window5.sub_window5_curve_preview_form import SubWindow5CurvePreviewForm


from Functions.steady_current_helper import curve_preview_five


# SubWindow5 - 319 Steady Current Helper
class SubWindow5(QWidget):
    def __init__(self, main_window: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.main_window = main_window
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
            '> Please drag the target file here...\n'
            '> Only .txt file is accepted...',
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

        button2 = QPushButton('Back',self)
        button2.clicked.connect(self.back)


        layout.addWidget(self.prompt_label)
        layout.addWidget(self.path_label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.button1)
        layout.addWidget(button2)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('319 - Steady Current Helper')

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
        self.button1.hide()

    def back(self):
        pos = self.pos()
        self.hide()
        self.reset_layout()
        self.main_window.move(pos)
        self.main_window.show()

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

        self.sub_window5_curve_preview_form = SubWindow5CurvePreviewForm(self)

        path = self.path_label.text().split('\n')[1]

        area = self.text_input.text()

        data_intime = curve_preview_five(path, area)

        img_bytes = data_intime[-1].read()

        img = QImage()
        img.loadFromData(img_bytes)

        pixmap = QPixmap.fromImage(img)
        pixmap_width = int(340 * get_scale_factor())
        pixmap_height = int(340 * get_scale_factor())
        pixmap = pixmap.scaled(
            pixmap_width,
            pixmap_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        result_text = '> Result\n'
        result_text += f'Name: {data_intime[0]}\n'
        result_text += f'Area: {data_intime[1]}\n'
        result_text += f'Jsc: {data_intime[2]}\n\n'
        result_text += ('I use the Least Squares Estimation to calculate the steady Jsc, '
                        'it is just a experimental function currently...')

        self.sub_window5_curve_preview_form.result.setText(result_text)
        self.sub_window5_curve_preview_form.preview.setPixmap(pixmap)

        self.sub_window5_curve_preview_form.preview.show()

        self.sub_window5_curve_preview_form.move(pos)
        self.sub_window5_curve_preview_form.show()












