from PyQt5.QtWidgets import QApplication


def get_scale_factor():
    base_width = 1920
    base_height = 1080
    base_logical_dpi = 96.0

    user_screen = QApplication.primaryScreen()
    user_screen_width = user_screen.geometry().width()
    user_screen_height = user_screen.geometry().height()
    user_logical_dpi = user_screen.logicalDotsPerInchX()

    system_scale_factor = user_screen.devicePixelRatio()

    screen_scale_factor_x = user_screen_width / base_width
    screen_scale_factor_y = user_screen_height / base_height
    screen_scale_factor = (screen_scale_factor_x + screen_scale_factor_y) / 2

    dpi_scale_factor = user_logical_dpi / base_logical_dpi

    scale_factor = (screen_scale_factor + dpi_scale_factor + system_scale_factor) / 3

    return scale_factor


