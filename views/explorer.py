import os.path
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QWidget, QGridLayout, QSplitter
from qframelesswindow import FramelessMainWindow, StandardTitleBar

from core.structs import AppActionTypes
from core.utils.assets_importer import qrcImage
from core.utils.helpers import getDirectorProperties, openFile
from core.utils.path_manager import PathManager
from core.utils.process_manager import ProcessManger
from models.sub_process_item_model import SubProcessItemModel
from views.components.menubar_widgets import VNavigationButtons, VOptionsButtons, VSearchBarWidget
from views.components.status_bar import VStatusBar
from views.sections.scene import V3DWindow
from views.sections.properties_panel import VPropertiesPanel


class FileExplorer(FramelessMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # define helpers
        self.pathManager = PathManager()
        self.processManager = ProcessManger()

        # define window components
        self.navigationButtons = VNavigationButtons()
        self.optionsButtons = VOptionsButtons()
        self.searchBarWidget = VSearchBarWidget()
        self.customStatusBar = VStatusBar()

        # add components to title bar
        self._titleBar = StandardTitleBar(self)
        self._titleBar.hBoxLayout.insertStretch(3, 1)
        self._titleBar.hBoxLayout.insertWidget(4, self.navigationButtons, 1, Qt.AlignmentFlag.AlignVCenter)
        self._titleBar.hBoxLayout.insertStretch(5, 1)
        self._titleBar.hBoxLayout.insertWidget(6, self.searchBarWidget, 1, Qt.AlignmentFlag.AlignLeft)
        self._titleBar.hBoxLayout.insertStretch(7, 1)
        self._titleBar.hBoxLayout.insertWidget(8, self.optionsButtons, 1, Qt.AlignmentFlag.AlignRight)

        # region - 3d scene
        self.view = V3DWindow()
        container3d = self.createWindowContainer(self.view)
        # endregion

        # region - props panel
        self.propsPanel = VPropertiesPanel()
        # endregion

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.addWidget(container3d)
        splitter.addWidget(self.propsPanel)
        splitter.setSizes([400, 120])

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

        self.resize(1000, 500)

        self._titleBar.raise_()
        self.__initialize()
        self.__configure()
        self.__connectSignals()

    # region initialize
    def __initialize(self):
        self.setStatusBar(self.customStatusBar)
        self.updateNavBar(self.pathManager.currentPath())
        self.customStatusBar.updateNumItems(self.pathManager.currentPath())
        self.propsPanel.stackedLayout.setCurrentIndex(1)

    # endregion

    # region configure
    def __configure(self):
        self.searchBarWidget.inputChanged.connect(self.__handleSearchButtonPressed)
        self.navigationButtons.actionTriggered.connect(self.__handleNavButtonsActions)
        self.view.currentDirectoryChanged.connect(self.__handleCurrentDirChanged)
        self.view.showOptions.connect(self.__handleShowItemProperties)
        self.view.openFile.connect(self.__handleOpenFile)

    # endregion

    # region workers
    def updateNavBar(self, path: str):
        """
        updates the navigation bar
        :param path:
        :return:
        """
        # changes the ssearch bar text
        self.searchBarWidget.setDirectoryInput(path)
        self.customStatusBar.updateNumItems(self.pathManager.currentPath())

        # update the navbar icons
        if self.pathManager.isOnlyPath():
            self.navigationButtons.backAction.setDisabled(True)
            self.navigationButtons.forwardAction.setDisabled(True)
            return

        if self.pathManager.isMiddlePath(path):
            self.navigationButtons.backAction.setDisabled(False)
            self.navigationButtons.forwardAction.setDisabled(False)
            return

        if self.pathManager.isLastPath(path):
            self.navigationButtons.backAction.setDisabled(False)
            self.navigationButtons.forwardAction.setDisabled(True)
            return

        if self.pathManager.isFirstPath(path):
            self.navigationButtons.backAction.setDisabled(True)
            self.navigationButtons.forwardAction.setDisabled(False)
            return

    # endregion

    # region setters

    # endregion

    # region getters

    # endregion

    # region helpers

    # endregion

    # region event handlers

    def __handleShowItemProperties(self, path: str):
        """
        shows the properties of the target file/dir
        :param path:
        :return:
        """
        self.propsPanel.hidePlaceholder()
        self.propsPanel.activeItemLabel.setText(str(Path(path).name))
        self.propsPanel.changePreviewIcon(path)

        def propFetchComplete(props):
            if not isinstance(props, list):
                print(props)
                return
            if len(props) == 0:
                return
            for i, items in enumerate(props):
                self.propsPanel.activeItemPropertiesTable.setItem(i, 0, items[0])
                self.propsPanel.activeItemPropertiesTable.setItem(i, 1, items[1])

        def propsFetchFailed(error):
            print("Failed with error", error)

        p = SubProcessItemModel('fetch_props', getDirectorProperties, path, propFetchComplete, propsFetchFailed,
                                name="GET_DIR_SIZE")
        self.processManager.launch(p)

    def __handleSearchButtonPressed(self, _=None):
        """
        takes path in the search bar and jumps to it
        :return:
        """
        path = self.searchBarWidget.directoryInput.text()
        if os.path.exists(path):
            self.pathManager.updatePaths(path)
            self.view.updateScene(path)
            self.updateNavBar(path)
        else:
            self.searchBarWidget.setDirectoryInput(self.pathManager.currentPath())

    def __handleNavButtonsActions(self, action: QAction):
        """
        handles actions from the navigation buttons
        :param action:
        :return:
        """
        p = None
        if action.data() == AppActionTypes.BACK:
            p = self.pathManager.previous()
            self.view.updateScene(p)
            self.searchBarWidget.setDirectoryInput(p)

        if action.data() == AppActionTypes.FORWARD:
            p = self.pathManager.next()
            self.view.updateScene(p)
            self.searchBarWidget.setDirectoryInput(p)

        if action.data() == AppActionTypes.UP:
            p = self.pathManager.currentPath()
            if p is None:
                return

            p = Path(p).parent
            if p is None:
                return
            p = str(p)
            self.pathManager.updatePaths(p)
            self.view.updateScene(p)
            self.searchBarWidget.setDirectoryInput(p)

        if action.data() == AppActionTypes.REFRESH:
            p = self.pathManager.currentPath()
            self.view.updateScene(p)

        if p is not None and os.path.exists(p):
            self.updateNavBar(p)

    def __handleCurrentDirChanged(self, path):
        self.pathManager.updatePaths(str(path))
        self.updateNavBar(str(path))
        self.propsPanel.hidePlaceholder()

    def __handleOpenFile(self, path):
        """
        opens the target file
        :param path:
        :return:
        """
        openFile(path)

    # endregion

    # region connect signals
    def __connectSignals(self):
        pass
    # endregion
