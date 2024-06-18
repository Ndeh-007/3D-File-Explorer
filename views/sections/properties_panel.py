from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QStackedLayout, QLabel, QVBoxLayout, QGridLayout

from core.utils.assets_importer import qrcImage
from views.components.placeholder_widget import VPlaceholderWidget
from views.components.properties_toolbar import PropertiesToolbar
from views.components.scroll_widget import VScrollWidget


class VPropertiesPanel(VScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent, mode="scroll")

        placeholder = VPlaceholderWidget(text="Empty")

        # region contents
        pixmap = QPixmap(qrcImage('folder')).scaled(100, 100)
        self.imageDirectoryIcon = QLabel()
        self.imageDirectoryIcon.setPixmap(pixmap)

        self.propsToolbar = PropertiesToolbar()

        self.propsGroupLayout = QGridLayout()
        propsGroup = QWidget()
        propsGroup.setLayout(self.propsGroupLayout)

        contentsLayout = QVBoxLayout()
        contentsLayout.setContentsMargins(0, 0, 0, 0)
        contentsLayout.addWidget(self.imageDirectoryIcon)
        contentsLayout.addWidget(self.propsToolbar)
        contentsLayout.addWidget(propsGroup)
        contentsLayout.addStretch()
        contentsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        contents = QWidget()
        contents.setLayout(contentsLayout)

        # endregion

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedLayout.addWidget(placeholder)
        self.stackedLayout.addWidget(contents)

        w = QWidget()
        w.setLayout(self.stackedLayout)
        self.setContentWidget(w)


