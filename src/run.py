import os
import sys

import plotly.graph_objs as go

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea

from GUI.window_scale import get_scale_factor

from GUI.sub_window1.sub_window1 import SubWindow1
from GUI.sub_window2.sub_window2 import SubWindow2
from GUI.sub_window3.sub_window3 import SubWindow3
from GUI.sub_window4.sub_window4 import SubWindow4
from GUI.sub_window5.sub_window5 import SubWindow5
from GUI.sub_window6.sub_window6 import SubWindow6


# Initial Kaleido
class InitialKaleido(QThread):
    status_signal = pyqtSignal(str)

    def run(self):
        fig = go.Figure()
        fig.write_image('initial.png', engine='kaleido')
        os.remove('initial.png')
        self.status_signal.emit('yes')


# Main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.9)
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

        self.pre_label = QLabel('Initializing...', self)

        self.button_1 = QPushButton('319 - IV Helper', self)
        self.button_1.clicked.connect(self.open_sub_window1)
        self.button_1.hide()

        self.button_2 = QPushButton('1428 - IV Helper', self)
        self.button_2.clicked.connect(self.open_sub_window2)
        self.button_2.hide()

        self.button_3 = QPushButton('319[1] - IV Helper', self)
        self.button_3.clicked.connect(self.open_sub_window3)
        self.button_3.hide()

        self.button_4 = QPushButton('317 - EQE Helper', self)
        self.button_4.clicked.connect(self.open_sub_window4)
        self.button_4.hide()

        self.button_5 = QPushButton('319 - Steady Current Helper', self)
        self.button_5.clicked.connect(self.open_sub_window5)
        self.button_5.hide()

        self.button_6 = QPushButton('About', self)
        self.button_6.clicked.connect(self.open_sub_window6)
        self.button_6.hide()

        layout.addWidget(self.pre_label)
        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)
        layout.addWidget(self.button_3)
        layout.addWidget(self.button_4)
        layout.addWidget(self.button_5)
        layout.addWidget(self.button_6)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('PV-Toolkit')

        self.sub_window1 = SubWindow1(self)
        self.sub_window2 = SubWindow2(self)
        self.sub_window3 = SubWindow3(self)
        self.sub_window4 = SubWindow4(self)
        self.sub_window5 = SubWindow5(self)
        self.sub_window6 = SubWindow6(self)

        self.initial_kaleido = InitialKaleido()
        self.initial_kaleido.status_signal.connect(self.update_layout)
        self.initial_kaleido.start()

    def update_layout(self, status_signal):
        if status_signal == 'yes':
            self.pre_label.setText(
                '> Ready for use...\n'
                '> Version: Release-1.0'
            )
            self.button_1.show()
            self.button_2.show()
            self.button_3.show()
            self.button_4.show()
            self.button_5.show()
            self.button_6.show()

    def open_sub_window1(self):
        pos = self.pos()
        self.hide()
        self.sub_window1.move(pos)
        self.sub_window1.show()

    def open_sub_window2(self):
        pos = self.pos()
        self.hide()
        self.sub_window2.move(pos)
        self.sub_window2.show()

    def open_sub_window3(self):
        pos = self.pos()
        self.hide()
        self.sub_window3.move(pos)
        self.sub_window3.show()

    def open_sub_window4(self):
        pos = self.pos()
        self.hide()
        self.sub_window4.move(pos)
        self.sub_window4.show()

    def open_sub_window5(self):
        pos = self.pos()
        self.hide()
        self.sub_window5.move(pos)
        self.sub_window5.show()

    def open_sub_window6(self):
        pos = self.pos()
        self.hide()
        self.sub_window6.move(pos)
        self.sub_window6.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
