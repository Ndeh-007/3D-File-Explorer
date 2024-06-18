import os
import platform
import time

import numpy as np
from PySide6.Qt3DCore import (Qt3DCore)
from PySide6.Qt3DExtras import (Qt3DExtras)
from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtCore import (QDir, Signal)
from PySide6.QtGui import (QVector3D, Qt)

from core.structs import LeafType
from models.leaf_click_options import LeafClickOptions
from models.tree_leaf_model import TreeLeafModel
from views.components.entities.tree_leaf import TreeLeaf


class V3DWindow(Qt3DExtras.Qt3DWindow):
    currentDirectoryChanged = Signal(str)

    def __init__(self):
        super().__init__()

        # define variables
        self.__leaves: dict[str, TreeLeaf] = {}
        self.__radius: int = 20
        self.__currentDir: str = "C:\\"

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
        self.constructScene()

    # endregion

    # region configure
    def __configure(self):
        pass

    # endregion

    # region event handlers

    def __handleLeafClicked(self, opts: LeafClickOptions):
        if opts.pickEvent.button() == Qt3DRender.QPickEvent.Buttons.LeftButton:
            self.__currentDir = opts.leafModel.path
            self.currentDirectoryChanged.emit(self.__currentDir)

            if os.path.isfile(self.__currentDir):
                return

            self.constructScene()

        if opts.pickEvent.button() == Qt3DRender.QPickEvent.Buttons.RightButton:
            pass

    def __handleUpVectorChanged(self, vector: QVector3D):
        pass

    # endregion

    # region workers

    @staticmethod
    def directoryType(path: str) -> LeafType:
        """
        gets the type of the directory
        :param path:
        :return:
        """

        def is_drive(_path):
            if platform.system() == "Windows":
                return len(path) == 2 and path[1] == ':'
            else:
                # Unix-like systems: Check if the path is a mount point
                return os.path.ismount(path)

        def test_path(_path: str):
            if os.path.isfile(_path):
                return LeafType.FILE
            elif os.path.isdir(_path):
                if is_drive(_path):
                    return LeafType.DRIVE
                else:
                    return LeafType.FOLDER
            else:
                return LeafType.UNSET

        return test_path(path)

    def clearScene(self):
        for key, leaf in self.__leaves.items():
            leaf.removeAllComponents()
            del leaf

        self.__leaves.clear()

    def constructScene(self):
        """
        takes in the particular directory and then positions them in 3d space.
        if dirPath is none, we are in the base directory
        :return:
        """
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
            leafModel = TreeLeafModel(path, dir_list[i], self.directoryType(path), path)
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
