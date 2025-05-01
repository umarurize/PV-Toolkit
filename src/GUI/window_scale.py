from PyQt5.QtWidgets import QApplication

def get_scale_factor():
    base_width = 1920
    base_height = 1080

    screen_geometry = QApplication.desktop().availableGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    scale_factor_x = screen_width / base_width
    scale_factor_y = screen_height / base_height
    scale_factor = min(scale_factor_x, scale_factor_y)

    return scale_factor


