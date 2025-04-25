import os
import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox


# SubWindow13 - Reload configurations
class SubWindow13(QWidget):
    def __init__(self, sub_window1):
        super().__init__()
        self.sub_window1 = sub_window1
        self.initUI()
        self.setFixedSize(400, 300)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        # Read config
        dir = os.getcwd()

        dir_1 = os.path.join(dir, 'configurations')
        if not os.path.exists(dir_1):
            os.mkdir(dir_1)

        dir_2 = os.path.join(dir_1, '319 - IV Helper')
        if not os.path.exists(dir_2):
            os.mkdir(dir_2)

        self.config_path = os.path.join(dir_2, 'config.json')

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config_data = json.loads(f.read())

        prompt_label = QLabel(
            '> Scanning range',
            self
        )

        self.config_label = QLabel(
            f'- low_to_high: {self.config_data["low_to_high"]}\n'
            f'- high_to_low: {self.config_data["high_to_low"]}',
            self
        )

        dropdown_label = QLabel(
            '> low_to_high\n'
            '- high_to_low will be auto changed...',
            self
        )

        self.dropdown_box = QComboBox()
        self.dropdown_box.addItems(['reverse', 'forward'])
        self.dropdown_box.currentIndexChanged.connect(self.on_change)

        button = QPushButton('Back', self)
        button.clicked.connect(self.back)

        layout.addWidget(prompt_label)
        layout.addWidget(self.config_label)
        layout.addWidget(dropdown_label)
        layout.addWidget(self.dropdown_box)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowIcon(icon)
        self.setWindowTitle('319 - Reload configurations')

    def on_change(self):
        low_to_high = self.dropdown_box.currentText()
        if low_to_high == 'reverse':
            high_to_low = 'forward'
        else:
            high_to_low = 'reverse'

        self.config_data = {
            "low_to_high": low_to_high,
            "high_to_low": high_to_low
        }
        json_str = json.dumps(self.config_data, indent=4, ensure_ascii=False)
        with open(self.config_path, 'w+', encoding='utf-8') as f:
            f.write(json_str)

        self.config_label.setText(
            f'- low_to_high: {self.config_data["low_to_high"]}\n'
            f'- high_to_low: {self.config_data["high_to_low"]}',
        )

    def back(self):
        pos = self.pos()
        self.hide()
        self.sub_window1.move(pos)
        self.sub_window1.show()












