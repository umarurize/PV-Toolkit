import json
import os
import sys
import plotly.graph_objs as go

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

from GUI.sub_window1.sub_window1 import SubWindow1
from GUI.sub_window2.sub_window2 import SubWindow2
from GUI.sub_window3.sub_window3 import SubWindow3
from GUI.sub_window4.sub_window4 import SubWindow4


# Main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFixedSize(400, 300)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        self.pre_label = QLabel('Initializing...', self)

        self.author_label = QLabel('Author: umarurize\n'
                                   'License: MIT 3.0\n'
                                   'Version: Alpha 0.1'
                                   '', self)
        self.author_label.hide()

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

        layout.addWidget(self.pre_label)
        layout.addWidget(self.author_label)
        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)
        layout.addWidget(self.button_3)
        layout.addWidget(self.button_4)

        self.setLayout(layout)
        self.setWindowTitle('PV-Toolkit')
        self.setWindowIcon(icon)

        self.sub_window1 = SubWindow1(self)
        self.sub_window2 = SubWindow2(self)
        self.sub_window3 = SubWindow3(self)
        self.sub_window4 = SubWindow4(self)

    def initial_kaleido(self):
        # Initial kaledio
        QApplication.processEvents()
        fig = go.Figure()
        fig.write_image('initial.png', engine='kaleido')
        os.remove('initial.png')
        self.pre_label.setText('Ready for use...')
        self.author_label.show()
        self.button_1.show()
        self.button_2.show()
        self.button_3.show()
        self.button_4.show()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.initial_kaleido()
    sys.exit(app.exec_())
