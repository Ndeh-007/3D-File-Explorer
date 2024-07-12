import os.path

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QStackedLayout, QLabel, QVBoxLayout, QGridLayout, QTableWidget

from core.utils.assets_importer import qrcImage
from views.components.placeholder_widget import VPlaceholderWidget
from views.components.properties_toolbar import PropertiesToolbar
from views.components.scroll_widget import VScrollWidget


class VPropertiesPanel(VScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent, mode="scroll")

        self.placeholder = VPlaceholderWidget(text="Empty")

        # region contents
        pixmap = QPixmap(qrcImage('folder')).scaled(100, 100)
        self.imageDirectoryIcon = QLabel()
        self.imageDirectoryIcon.setPixmap(pixmap)

        self.propsToolbar = PropertiesToolbar()

        self.propsGroupLayout = QGridLayout()
        propsGroup = QWidget()
        propsGroup.setLayout(self.propsGroupLayout)

        self.activeItemLabel = QLabel()
        self.activeItemPropertiesTable = QTableWidget()
        self.activeItemPropertiesTable.setRowCount(4)
        self.activeItemPropertiesTable.setColumnCount(2)
        self.activeItemPropertiesTable.horizontalHeader().hide()
        self.activeItemPropertiesTable.verticalHeader().hide()
        self.activeItemPropertiesTable.horizontalHeader().setStretchLastSection(True)

        contentsLayout = QVBoxLayout()
        contentsLayout.addWidget(self.imageDirectoryIcon)
        contentsLayout.addWidget(self.propsToolbar)
        contentsLayout.addWidget(propsGroup)
        # contentsLayout.addStretch()
        contentsLayout.addWidget(self.activeItemLabel)
        contentsLayout.addWidget(self.activeItemPropertiesTable)
        contentsLayout.addStretch()

        contentsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        contents = QWidget()
        contents.setLayout(contentsLayout)

        # endregion

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedLayout.addWidget(self.placeholder)
        self.stackedLayout.addWidget(contents)

        w = QWidget()
        w.setLayout(self.stackedLayout)
        self.setContentWidget(w)

        self.propsToolbar.hide()

    def showPlaceholder(self):
        self.stackedLayout.setCurrentIndex(0)

    def hidePlaceholder(self):
        self.stackedLayout.setCurrentIndex(1)

    def changePreviewIcon(self, path: str):
        """
        changes the preview icon
        :param path:
        :return:
        """
        if not os.path.exists(path):
            return
        if os.path.isfile(path):
            self.togglePreviewIcon("file")
        if os.path.isdir(path):
            self.togglePreviewIcon("folder")

    def togglePreviewIcon(self, mode: str = "folder"):
        """
        switches the preview icon
        :param mode:
        :return:
        """
        pixmap = None
        if mode == "folder":
            pixmap = QPixmap(qrcImage('folder')).scaled(100, 100)

        if mode == "file":
            pixmap = QPixmap(qrcImage('file')).scaled(100, 100)

        self.imageDirectoryIcon.setPixmap(pixmap)
