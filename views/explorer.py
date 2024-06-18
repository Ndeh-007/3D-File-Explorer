from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QWidget, QGridLayout, QSplitter
from qframelesswindow import FramelessMainWindow, StandardTitleBar

from core.structs import AppActionTypes
from core.utils.assets_importer import qrcImage
from core.utils.path_manager import PathManager
from views.components.menubar_widgets import VNavigationButtons, VOptionsButtons, VSearchBarWidget
from views.sections.scene import V3DWindow
from views.sections.properties_panel import VPropertiesPanel


class FileExplorer(FramelessMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # define helpers
        self.pathManager = PathManager()

        # define window components
        self.navigationButtons = VNavigationButtons()
        self.optionsButtons = VOptionsButtons()
        self.searchBarWidget = VSearchBarWidget()

        # add components to title bar
        self._titleBar = StandardTitleBar(self)
        self._titleBar.hBoxLayout.insertStretch(3, 1)
        self._titleBar.hBoxLayout.insertWidget(4, self.navigationButtons, 1,  Qt.AlignmentFlag.AlignVCenter)
        self._titleBar.hBoxLayout.insertStretch(5, 1)
        self._titleBar.hBoxLayout.insertWidget(6, self.searchBarWidget, 1, Qt.AlignmentFlag.AlignLeft)
        self._titleBar.hBoxLayout.insertStretch(7, 1)
        self._titleBar.hBoxLayout.insertWidget(8, self.optionsButtons, 1, Qt.AlignmentFlag.AlignRight)

        # region - 3d scene
        self.view = V3DWindow()
        self.view.currentDirectoryChanged.connect(self.__handleCurrentDirChanged)
        container3d = self.createWindowContainer(self.view)
        # endregion

        # region - props panel
        self.propsPanel = VPropertiesPanel()
        # endregion

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.addWidget(container3d)
        splitter.addWidget(self.propsPanel)
        splitter.setSizes([400, 100])

        # Set up the layout
        layout = QGridLayout()
        layout.setContentsMargins(0, 35, 0, 0)
        layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # define app window props
        windowIcon = QIcon(qrcImage('logo', 'ico'))
        self.setWindowIcon(windowIcon)

        self.setTitleBar(self._titleBar)
        self.setWindowTitle("FileTree")

        self.resize(1000, 800)

        self._titleBar.raise_()
        self.__initialize()
        self.__configure()
        self.__connectSignals()

    # region initialize
    def __initialize(self):
        self.propsPanel.stackedLayout.setCurrentIndex(1)

    # endregion

    # region configure
    def __configure(self):
        self.navigationButtons.actionTriggered.connect(self.__handleNavButtonsActions)
    # endregion

    # region workers
    def updateNavBar(self, path: str):
        """
        updates the navigation bar
        :param path:
        :return:
        """
        # changes the ssearch bar text
        self.searchBarWidget.setSearchInput(path)

        # update the navbar icons
        if self.pathManager.isOnlyPath():
            self.navigationButtons.backAction.setDisabled(True)
            self.navigationButtons.forwardAction.setDisabled(True)

        if self.pathManager.isMiddlePath(path):
            self.navigationButtons.backAction.setDisabled(False)
            self.navigationButtons.forwardAction.setDisabled(False)

        if self.pathManager.isLastPath(path):
            self.navigationButtons.backAction.setDisabled(False)
            self.navigationButtons.forwardAction.setDisabled(True)

        if self.pathManager.isFirstPath(path):
            self.navigationButtons.backAction.setDisabled(True)
            self.navigationButtons.forwardAction.setDisabled(False)

    # endregion

    # region setters

    # endregion

    # region getters

    # endregion

    # region helpers

    # endregion

    # region event handlers

    def __handleNavButtonsActions(self, action: QAction):
        """
        handles actions from the navigation buttons
        :param action:
        :return:
        """

        if action.data() == AppActionTypes.BACK:
            path = self.pathManager.previous()
            self.view.updateScene(path)
            self.searchBarWidget.setSearchInput(path)

        if action.data() == AppActionTypes.FORWARD:
            path = self.pathManager.next()
            self.view.updateScene(path)
            self.searchBarWidget.setSearchInput(path)

        if action.data() == AppActionTypes.UP:
            p = self.pathManager.currentPath()
            if p is None:
                return
            path = Path(p).parent
            self.view.updateScene(str(path))
            self.searchBarWidget.setSearchInput(str(path))

        if action.data() == AppActionTypes.REFRESH:
            self.view.constructScene()

    def __handleCurrentDirChanged(self, path):
        self.pathManager.updatePaths(str(path))
        self.updateNavBar(str(path))

    # endregion

    # region connect signals
    def __connectSignals(self):
        pass
    # endregion

