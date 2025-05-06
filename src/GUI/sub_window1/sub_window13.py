import os
import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QScrollArea

from GUI.window_scale import get_scale_factor


# SubWindow13 - Reload configurations
class SubWindow13(QWidget):
    def __init__(self, sub_window1: QWidget):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.sub_window1 = sub_window1
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
        layout.setSpacing(10)

        icon = QIcon('resources/logo.ico')

        font = QFont()
        font_size = int(8 * get_scale_factor())
        font.setPointSize(font_size)
        font.setFamily('Microsoft YaHei')

        # Read config
        dir = os.getcwd()

        dir_1 = os.path.join(dir, 'configurations')
        if not os.path.exists(dir_1):
            os.mkdir(dir_1)

        dir_2 = os.path.join(dir_1, '319 - IV Helper')
        if not os.path.exists(dir_2):
            os.mkdir(dir_2)

        self.config_path = os.path.join(dir_2, 'config.json')

        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w', encoding='utf-8') as f:
                config_data = {
                    'low_to_high': 'reverse',
                    'high_to_low': 'forward'
                }
                json_str = json.dumps(config_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.loads(f.read())
        self.config_data = config_data

        prompt_label = QLabel(
            '> Scanning range',
            self
        )

        self.config_label = QLabel(
            f'- low_to_high: <span style="color:red">{self.config_data["low_to_high"]}</span><br>'
            f'- high_to_low: <span style="color:red">{self.config_data["high_to_low"]}</span>',
            self
        )

        dropdown_label = QLabel(
            '> low_to_high\n'
            '- high_to_low will be auto changed...',
            self
        )

        self.dropdown_box = QComboBox()
        if self.config_data['low_to_high'] == 'reverse':
            self.dropdown_box.addItems(['reverse', 'forward'])
        else:
            self.dropdown_box.addItems(['forward', 'reverse'])
        self.dropdown_box.currentIndexChanged.connect(self.on_change)

        button = QPushButton('Save and back', self)
        button.clicked.connect(self.back)

        layout.addWidget(prompt_label)
        layout.addWidget(self.config_label)
        layout.addWidget(dropdown_label)
        layout.addWidget(self.dropdown_box)
        layout.addWidget(button)

        scroll_area.setWidget(function_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setWindowIcon(icon)
        self.setFont(font)
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
            f'- low_to_high: <span style="color:red">{self.config_data["low_to_high"]}</span><br>'
            f'- high_to_low: <span style="color:red">{self.config_data["high_to_low"]}</span>',
        )

    def back(self):
        pos = self.pos()
        self.hide()
        self.sub_window1.move(pos)
        self.sub_window1.show()












