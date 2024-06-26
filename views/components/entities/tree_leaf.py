from PySide6.Qt3DCore import (Qt3DCore)
from PySide6.Qt3DExtras import (Qt3DExtras)
from PySide6.Qt3DRender import (Qt3DRender)
from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtGui import (QMatrix4x4, QQuaternion, QVector3D, QFont, QColor)

from models.leaf_click_options import LeafClickOptions
from models.tree_leaf_model import TreeLeafModel


class LookAtTransform(Qt3DCore.QTransform):
    def __init__(self, camera: Qt3DRender.QCamera, scale: float = 1.0,
                 pos: QVector3D = QVector3D(0, 0, 0), parent: QObject = None):
        super().__init__(parent)
        self.camera = camera
        self.target = QVector3D(0, 0, 0)
        self.__pos = pos
        self.__scale = scale
        self.update_rotation()

        self.camera.positionChanged.connect(self.update_rotation)
        self.camera.viewCenterChanged.connect(self.update_rotation)

    def setCameraTransformTarget(self, target: QVector3D):
        self.target = target
        self.update_rotation()

    @Slot()
    def update_rotation(self):
        forward = (self.camera.position() - self.target).normalized()
        up = QVector3D(0.0, 1.0, 0.0)  # Assuming Y-up coordinate system
        right = QVector3D.crossProduct(up, forward).normalized()
        up = QVector3D.crossProduct(forward, right).normalized()

        rotation_matrix = QMatrix4x4(
            right.x(), up.x(), forward.x(), 0.0,
            right.y(), up.y(), forward.y(), 0.0,
            right.z(), up.z(), forward.z(), 0.0,
            0.0, 0.0, 0.0, 1.0
        )
        self.setMatrix(rotation_matrix)
        self.setScale(self.__scale)
        self.setTranslation(self.__pos)

    def setPosition(self, pos: QVector3D):
        self.__pos = pos

    def pos(self):
        return self.__pos

    def setScale(self, scale: float) -> None:
        self.__scale = scale
        super().setScale(scale)


class TreeLeaf(QObject):
    clicked = Signal(LeafClickOptions)

    def __init__(self, parentEntity, camera: Qt3DRender.QCamera, model: TreeLeafModel = None):
        super().__init__()

        self.parentEntity = parentEntity
        self.model = model

        self.highlightColor = "#2dbd3e"  # neon green
        self.baseIconColor = QColor(0, 0, 0)  # default black
        self.baseTextColor = QColor(255, 0, 0)  # red
        self.baseShine = 5
        self.baseIconScale = 1.0
        self.baseTextScale = 0.5

        if model is None:
            self.model = TreeLeafModel()

        # region Icon Entity
        self.iconEntity = Qt3DCore.QEntity(self.parentEntity)
        self.iconMesh = Qt3DExtras.QCuboidMesh(self.parentEntity)

        if self.model.isFile():
            self.iconMesh = Qt3DRender.QMesh(self.parentEntity)
            self.iconMesh.setSource(QUrl("qrc:/meshes/file_light.obj"))
        if self.model.isFolder():
            self.iconMesh = Qt3DRender.QMesh(self.parentEntity)
            self.iconMesh.setSource(QUrl("qrc:/meshes/folder_light.obj"))

        self.iconObjectPicker = Qt3DRender.QObjectPicker(self.parentEntity)
        self.iconMaterial = Qt3DExtras.QPhongMaterial(self.parentEntity)
        if model.isFile():
            self.baseIconColor = QColor(50, 130, 246)  # blue
        if model.isDrive():
            self.baseIconColor = QColor(128, 128, 128)  # grey
        if model.isFolder():
            self.baseIconColor = QColor(255, 201, 14)  # yellow

        self.iconMaterial.setDiffuse(self.baseIconColor)
        self.iconMaterial.setAmbient(self.baseIconColor)
        # self.iconMaterial.setSpecular(self.baseIconColor)
        self.iconMaterial.setShininess(self.baseShine)

        self.iconTransform = LookAtTransform(camera, parent=self.parentEntity)

        self.iconEntity.addComponent(self.iconMesh)
        self.iconEntity.addComponent(self.iconObjectPicker)
        self.iconEntity.addComponent(self.iconTransform)
        self.iconEntity.addComponent(self.iconMaterial)

        # endregion

        # region text
        # define the text entity
        self.textEntity = Qt3DCore.QEntity(self.parentEntity)
        self.textMaterial = Qt3DExtras.QPhongMaterial(self.parentEntity)
        self.textMaterial.setDiffuse(self.baseTextColor)

        self.textTransform = LookAtTransform(camera, scale=0.4, parent=self.parentEntity)
        self.textTransform.rotationChanged.connect(self.handleTextRotationChanged)
        self.textTransform.scaleChanged.connect(self.handleTextScaleChanged)
        self.textTransform.matrixChanged.connect(self.handleTextRotationMatrixChanged)

        self.textMesh = Qt3DExtras.QExtrudedTextMesh(self.parentEntity)
        self.textMesh.setText(model.text)
        self.textMesh.setDepth(0.01)
        self.textMesh.setFont(QFont('monospace'))

        self.textEntity.addComponent(self.textMaterial)
        self.textEntity.addComponent(self.textMesh)
        self.textEntity.addComponent(self.textTransform)
        # endregion

        self.iconObjectPicker.clicked.connect(self.__handleClick)

    def moveTo(self, pos: QVector3D):
        """
        moves the leaf to the target position
        :param pos:
        :return:
        """
        p, q = self.model.computeIconTextPositions(pos)

        self.iconTransform.setPosition(p)
        self.textTransform.setPosition(q)

        self.iconTransform.update_rotation()
        self.textTransform.update_rotation()

    def __handleClick(self, event: Qt3DRender.QPickEvent):
        """
        collects click event and emits a signal carrying the click information
        :param event:
        :return:
        """
        opts = LeafClickOptions(self.model, event)
        self.clicked.emit(opts)

    def handleTextRotationChanged(self, rotation: QQuaternion):
        return

    def handleTextRotationMatrixChanged(self):
        return

    def handleTextScaleChanged(self, scale: float):
        return

    def setEnabled(self, state):
        self.iconEntity.setEnabled(state)
        self.textEntity.setEnabled(state)

    def removeAllComponents(self):
        self.iconEntity.removeComponent(self.iconMesh)
        self.iconEntity.removeComponent(self.iconObjectPicker)
        self.iconEntity.removeComponent(self.iconTransform)
        self.iconEntity.removeComponent(self.iconMaterial)

        self.textEntity.removeComponent(self.textMaterial)
        self.textEntity.removeComponent(self.textMesh)
        self.textEntity.removeComponent(self.textTransform)

    def highlight(self):
        """
        changes the color of the leaf to the highlight color
        :return:
        """
        self.iconMaterial.setDiffuse(self.highlightColor)
        self.iconMaterial.setAmbient(self.highlightColor)
        self.iconMaterial.setSpecular(self.highlightColor)
        self.iconMaterial.setShininess(10)

        self.textMaterial.setDiffuse(self.highlightColor)
        self.textMaterial.setAmbient(self.highlightColor)
        self.textMaterial.setSpecular(self.highlightColor)
        self.textMaterial.setShininess(10)

    def removeHighlight(self):
        """
        removes the highlight from the leaf
        :return:
        """
        self.iconMaterial.setDiffuse(self.baseIconColor)
        self.iconMaterial.setAmbient(self.baseIconColor)
        self.iconMaterial.setShininess(self.baseShine)

        self.textMaterial.setDiffuse(self.baseTextColor)
        self.textMaterial.setAmbient(self.baseTextColor)
        self.textMaterial.setShininess(self.baseShine)
