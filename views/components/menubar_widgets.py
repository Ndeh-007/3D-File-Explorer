import os.path

import qtawesome
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction, QKeyEvent, Qt
from PySide6.QtWidgets import QToolBar, QWidget, QLineEdit, QGridLayout, QPushButton

from core.structs import AppActionTypes


class VNavigationButtons(QToolBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        self.backAction = QAction(self)
        self.forwardAction = QAction(self)
        self.upwardAction = QAction(self)
        self.refreshAction = QAction(self)

        self.backAction.setData(AppActionTypes.BACK)
        self.forwardAction.setData(AppActionTypes.FORWARD)
        self.upwardAction.setData(AppActionTypes.UP)
        self.refreshAction.setData(AppActionTypes.REFRESH)

        backIcon = qtawesome.icon("msc.arrow-left")
        forwardIcon = qtawesome.icon("msc.arrow-right")
        upIcon = qtawesome.icon("msc.arrow-up")
        refreshIcon = qtawesome.icon("msc.refresh")

        self.backAction.setIcon(backIcon)
        self.forwardAction.setIcon(forwardIcon)
        self.upwardAction.setIcon(upIcon)
        self.refreshAction.setIcon(refreshIcon)

        self.addAction(self.backAction)
        self.addSeparator()
        self.addAction(self.forwardAction)
        self.addSeparator()
        self.addAction(self.upwardAction)
        self.addSeparator()
        self.addAction(self.refreshAction)


class VOptionsButtons(QToolBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        settingsAction = QAction(self)
        propertiesAction = QAction(self)

        settingsAction.setData(AppActionTypes.SETTINGS)
        propertiesAction.setData(AppActionTypes.PROPERTIES)

        propertiesIcon = qtawesome.icon("msc.kebab-vertical")
        settingsIcon = qtawesome.icon("msc.settings-gear")

        settingsAction = QAction(self)
        propertiesAction = QAction(self)

        settingsAction.setIcon(settingsIcon)
        propertiesAction.setIcon(propertiesIcon)

        self.addAction(propertiesAction)
        self.addSeparator()
        self.addAction(settingsAction)


class VSearchBarWidget(QWidget, QObject):
    inputChanged = Signal(str)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        # region UI
        self.directoryInput = QLineEdit()
        self.directoryInput.setPlaceholderText("Jump to Directory")

        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search...")

        self.jumpButton = QPushButton()
        searchIcon = qtawesome.icon('msc.arrow-right')
        self.jumpButton.setIcon(searchIcon)

        layout = QGridLayout()
        layout.addWidget(self.directoryInput, 0, 0)
        layout.addWidget(self.jumpButton, 0, 1)
        layout.addWidget(self.searchInput, 1, 0)
        layout.setColumnStretch(0, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # endregion

        self.__initialize()
        self.__configure()

    def __initialize(self):
        self.searchInput.hide()

    def __configure(self):
        self.directoryInput.textChanged.connect(self.__handleDirectoryTextChanged)
        self.jumpButton.pressed.connect(self.__handleJumpButtonPressed)
        self.directoryInput.editingFinished.connect(self.__editingFinished)

    def setDirectoryInput(self, value: str):
        self.directoryInput.setText(value)

    def __handleDirectoryTextChanged(self, text):
        pass

    def __editingFinished(self):
        self.__handleJumpButtonPressed()

    def __handleJumpButtonPressed(self):
        path = self.directoryInput.text()
        self.inputChanged.emit(path)
