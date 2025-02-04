import os

import numpy as np
from PySide6.Qt3DCore import (Qt3DCore)
from PySide6.Qt3DExtras import (Qt3DExtras)
from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtCore import (Signal, QDir)
from PySide6.QtGui import (QVector3D)

from core.utils.helpers import directoryType
from models.leaf_click_options import LeafClickOptions
from models.tree_leaf_model import TreeLeafModel
from views.components.entities.floating_grid import FloatingGrid
from views.components.entities.tree_leaf import TreeLeaf


class V3DWindow(Qt3DExtras.Qt3DWindow):
    currentDirectoryChanged = Signal(str)
    showOptions = Signal(str)
    openFile = Signal(str)

    def __init__(self):
        super().__init__()

        # define variables
        self.__leaves: dict[str, TreeLeaf] = {}
        self.__radius: int = 20
        self.__currentDir: str = QDir.rootPath()
        self.__others: dict[str, object] = {}
        self.__activeLeafPid: str = QDir.rootPath()

        # region - create scene

        # Root entity
        self.rootEntity = Qt3DCore.QEntity()

        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 40))
        self.camera().setViewCenter(QVector3D(0, 0, 0))

        # For camera controls
        self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        self.camController.setLinearSpeed(50)
        self.camController.setLookSpeed(180)
        self.camController.setCamera(self.camera())
        self.camController.setInversePan(True)
        self.camController.setInverseXTranslate(True)
        self.camController.setInverseYTranslate(True)
        self.camController.setInverseTilt(True)
        self.camController.upVectorChanged.connect(self.__handleUpVectorChanged)
        self.setRootEntity(self.rootEntity)
        # endregion

        self.__initialize()
        self.__configure()

    # regin initialize
    def __initialize(self):
        # self.constructGrid()
        self.constructScene()

    # endregion

    # region configure
    def __configure(self):
        pass

    # endregion

    # region event handlers

    def __handleLeafClicked(self, opts: LeafClickOptions):
        if opts.pickEvent.button() == Qt3DRender.QPickEvent.Buttons.LeftButton:
            if os.path.isfile(opts.leafModel.path):
                self.openFile.emit(opts.leafModel.path)
                return

            self.__currentDir = opts.leafModel.path
            self.currentDirectoryChanged.emit(self.__currentDir)

            self.constructScene()

        if opts.pickEvent.button() == Qt3DRender.QPickEvent.Buttons.RightButton:
            self.showOptions.emit(opts.leafModel.path)

        self.highlightLeaf(opts.leafModel.pid)

    def __handleUpVectorChanged(self, vector: QVector3D):
        pass

    # endregion

    # region

    def highlightLeaf(self, pid: str):
        """
        changes the color of a particular leaf to indicate that it has been interacted with
        :param pid: the id of the leaf to be lighted
        :return:
        """

        # remove previous highlight
        prevLeaf = self.__leaves.get(self.__activeLeafPid)
        if prevLeaf is not None:
            prevLeaf.removeHighlight()

        leaf = self.__leaves.get(pid)
        if leaf is None:
            return False

        leaf.highlight()
        self.__activeLeafPid = pid

    def clearScene(self):
        for key, leaf in self.__leaves.items():
            leaf.removeAllComponents()
            del leaf

        self.__leaves.clear()

    def constructGrid(self):
        """
        creates a grid and throws it in space
        :return:
        """
        grid = FloatingGrid(self.rootEntity, self.camera())
        grid.moveTo(QVector3D(0, 0, 0))
        self.__others.update({"grid": grid})

    def constructScene(self):
        """
        takes in the particular directory and then positions them in 3d space.
        if dirPath is none, we are in the base directory
        :return:
        """
        # return

        self.clearScene()

        phi = np.pi * (3. - np.sqrt(5.))

        dir_list = os.listdir(self.__currentDir)
        n = len(dir_list)

        for i in range(n):
            # compute pos
            y = 1 - (i / float((n + 1) - 1)) * 2  # y goes from 1 to -1
            radius_slice = np.sqrt(1 - y * y)  # radius at y

            theta = phi * i  # golden angle increment

            x = np.cos(theta) * radius_slice
            z = np.sin(theta) * radius_slice

            pos = QVector3D(x * self.__radius, y * self.__radius, z * self.__radius)

            # create leaf
            path = os.path.join(self.__currentDir, dir_list[i])
            leafModel = TreeLeafModel(path, dir_list[i], directoryType(path), path)
            leaf = TreeLeaf(self.rootEntity, self.camera(), leafModel)
            leaf.clicked.connect(self.__handleLeafClicked)

            # translate
            leaf.moveTo(pos)

            # save
            self.__leaves.update({leafModel.pid: leaf})

    def updateScene(self, path: str):
        """

        :param path:
        :return:
        """
        if not os.path.exists(path):
            return

        if os.path.isfile(path):
            return

        self.__currentDir = path
        self.constructScene()

    # endregion
