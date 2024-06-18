from typing import Literal

from PySide6.QtWidgets import QFrame, QVBoxLayout, QScrollArea, QStackedWidget, QWidget


class VScrollWidget(QFrame):
    def __init__(self, parent=None, mode: Literal['scroll', 'static'] = 'scroll'):
        super().__init__(parent)

        self.__mode = mode

        self.contentWidget = QScrollArea()
        if self.__mode == "static":
            self.contentWidget = QStackedWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.contentWidget)
        self.setLayout(layout)

    def setContentWidget(self, widget: QWidget):
        """
        sets the content widget
        :param widget:
        :return:
        """
        if self.__mode == 'scroll' and isinstance(self.contentWidget, QScrollArea):
            self.contentWidget.setWidget(widget)
            self.contentWidget.setFrameShape(QFrame.Shape.NoFrame)
            self.contentWidget.setWidgetResizable(True)

        if self.__mode == 'static' and isinstance(self.contentWidget, QStackedWidget):
            self.contentWidget.addWidget(widget)

