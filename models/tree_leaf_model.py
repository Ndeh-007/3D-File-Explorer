from uuid import uuid4

from PySide6.QtGui import QVector3D

from core.structs import LeafType


class TreeLeafModel:
    def __init__(self, path: str = None, text: str = "Unset", leafType: LeafType = LeafType.UNSET, pid: str = None):
        self.path: str = path

        self.text: str = text
        self.leafType: LeafType = leafType

        self.pid: str = pid
        if pid is None:
            self.pid = str(uuid4())

        self.iconHeight = 30
        self.textHeight = 10
        self.separation = 1.2

    def computeIconTextPositions(self, pos: QVector3D) -> tuple[QVector3D, QVector3D]:
        """
        Given a particular position in space, compute the positions of the corresponding icon
        and its label
        :param pos:
        :return: the (iconPosition, textPosition)
        """
        # the icon takes the position
        iPos = pos

        # collect the positions
        tPos = QVector3D(0, -self.separation, 0)

        return iPos, tPos

    def textPosition(self):
        """
        gets the text position, shifted from its parent
        :return:
        """
        return QVector3D(0, -self.separation, 0)

    def isFile(self) -> bool:
        return self.leafType == LeafType.FILE

    def isFolder(self) -> bool:
        return self.leafType == LeafType.FOLDER

    def isDrive(self) -> bool:
        return self.leafType == LeafType.DRIVE

    def isUnknown(self) -> bool:
        return self.leafType == LeafType.UNSET
