import os
import sys
import plotly.graph_objs as go

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

from GUI.sub_window1.sub_window1 import SubWindow1
from GUI.sub_window2.sub_window2 import SubWindow2


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
                                   'Version: Alapa 0.1'
                                   '', self)
        self.author_label.hide()

        self.button_1 = QPushButton('319 - IV Helper', self)
        self.button_1.clicked.connect(self.open_sub_window1)
        self.button_1.hide()

        self.button_2 = QPushButton('1428 - IV Helper', self)
        self.button_2.clicked.connect(self.open_sub_window2)
        self.button_2.hide()

        layout.addWidget(self.pre_label)
        layout.addWidget(self.author_label)
        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)

        self.setLayout(layout)
        self.setWindowTitle('PV-Toolkit')
        self.setWindowIcon(icon)

        self.sub_window1 = SubWindow1(self)
        self.sub_window2 = SubWindow2(self)

    def initial_kaleido(self):
        QApplication.processEvents()
        fig = go.Figure()
        fig.write_image('initial.png', engine='kaleido')
        os.remove('initial.png')
        self.pre_label.setText('Ready for use...')
        self.author_label.show()
        self.button_1.show()
        self.button_2.show()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.initial_kaleido()
    sys.exit(app.exec_())
