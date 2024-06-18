from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class AppColorsRBG:
    def __init__(self):
        self.white_rgb = "#ffffff"
        self.black_rgb = "#000000"

        self.primary_rbg = "#219DD2"
        self.primary_tint_rbg = "#6370ff"
        self.primary_shade_rbg = "#4854e0"

        self.secondary_rbg = "#5260ff"
        self.secondary_tint_rbg = "#DFF6FF"
        self.secondary_shade_rbg = "#c4d8e0"

        self.tertiary_rbg = "#5260ff"
        self.tertiary_tint_rbg = "#6370ff"
        self.tertiary_shade_rbg = "#4854e0"

        self.success_rbg = "#2dd36f"
        self.success_tint_rbg = "#42d77d"
        self.success_shade_rbg = "#28ba62"

        self.danger_rbg = "#eb445a"
        self.danger_tint_rbg = "#eb445a"
        self.danger_shade_rbg = "#eb445a"

        self.warning_rbg = "#ffc409"
        self.warning_tint_rbg = "#ffca22"
        self.warning_shade_rbg = "#e0ac08"

        self.medium_rbg = "#92949c"
        self.medium_tint_rbg = "#9d9fa6"
        self.medium_shade_rbg = "#808289"

        self.light_rbg = "#f4f5f8"
        self.light_tint_rbg = "#f5f6f9"
        self.light_shade_rbg = "#d7d8da"

        self.dark_rbg = "#222428"
        self.dark_tint_rbg = "#383a3e"
        self.dark_shade_rbg = "#1e2023"

        self.color_keys = {
            "white_rbg": "#ffffff",
            "black_rbg": "#000000",

            "primary_rbg": "#219DD2",
            "primary_tint_rbg": "#6370ff",
            "primary_shade_rbg": "#4854e0",

            "secondary_rbg": "#5260ff",
            "secondary_tint_rbg": "#DFF6FF",
            "secondary_shade_rbg": "#c4d8e0",

            "tertiary_rbg": "#5260ff",
            "tertiary_tint_rbg": "#6370ff",
            "tertiary_shade_rbg": "#4854e0",

            "success_rbg": "#2dd36f",
            "success_tint_rbg": "#42d77d",
            "success_shade_rbg": "#28ba62",

            "danger_rbg": "#eb445a",
            "danger_tint_rbg": "#eb445a",
            "danger_shade_rbg": "#eb445a",

            "warning_rbg": "#ffc409",
            "warning_tint_rbg": "#ffca22",
            "warning_shade_rbg": "#e0ac08",

            "medium_rbg": "#92949c",
            "medium_tint_rbg": "#9d9fa6",
            "medium_shade_rbg": "#808289",

            "light_rbg": "#f4f5f8",
            "light_tint_rbg": "#f5f6f9",
            "light_shade_rbg": "#d7d8da",

            "dark_rbg": "#222428",
            "dark_tint_rbg": "#383a3e",
            "dark_shade_rbg": "#1e2023"
        }


appColors = AppColorsRBG()
