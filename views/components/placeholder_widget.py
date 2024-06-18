from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class VPlaceholderWidget(QWidget):
    def __init__(self, parent: QWidget = None, text: str = ""):
        super().__init__(parent=parent)

        self.placeholderLabel = QLabel(text)
        self.placeholderLabel.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.placeholderLabel)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def setText(self, text: str):
        """
        sets the text of the placeholder label
        :param text:
        :return:
        """
        if text is None:
            return
        self.placeholderLabel.setText(text)
