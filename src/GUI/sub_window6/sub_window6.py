import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea

from GUI.window_scale import get_scale_factor


class SubWindow6(QWidget):
    def __init__(self, main_window: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.main_window = main_window
        self.initUI()
        self.setFixedSize(
            int(400 * get_scale_factor()),
            int(335 * get_scale_factor())
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

        author_label = QLabel(
            'Author: umarurize\n'
            'License: Apache-2.0\n'
            'Version: Release-1.0',
            self
        )

        avatar_label = QLabel(self)

        dir = os.getcwd()
        avatar_path = os.path.join(dir, 'resources', 'avatar.png')

        with open(avatar_path, 'rb') as f:
            img_bytes = f.read()

        avatar_img = QImage()
        avatar_img.loadFromData(img_bytes)

        pixmap = QPixmap.fromImage(avatar_img)
        pixmap_width = int(75 * get_scale_factor())
        pixmap_height = int(75 * get_scale_factor())
        pixmap = pixmap.scaled(pixmap_width,
                               pixmap_height,
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)

        avatar_label.setPixmap(pixmap)

        author_label1 = QLabel(
            'Group: 1 kW·h Group<br>'
            'Contact: 3229187183@qq.com<br>'
            'Repo-link: '
            '<a href="https://github.com/umarurize/PV-Toolkit" >PV-Toolkit (Github)</a>',
            self
        )
        author_label1.setOpenExternalLinks(True)

        author_label2 = QLabel(
            '<span style="color:red">Warning:</span><br>'
            'This toolkit is customized for FUNSOM of Soochow.U and may not be fully'
            ' applicable. If you have other requirements, you can contact me for customizations...',
            self
        )
        author_label2.setWordWrap(True)

        button = QPushButton('Back', self)
        button.clicked.connect(self.back)

        layout.addWidget(author_label)
        layout.addWidget(avatar_label)
        layout.addWidget(author_label1)
        layout.addWidget(author_label2)
        layout.addWidget(button)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
        self.setWindowTitle('About')

    def back(self):
        pos = self.pos()
        self.hide()
        self.main_window.move(pos)
        self.main_window.show()
