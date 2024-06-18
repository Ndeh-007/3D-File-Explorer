from PySide6.Qt3DCore import (Qt3DCore)
from PySide6.Qt3DExtras import (Qt3DExtras)
from PySide6.Qt3DRender import (Qt3DRender)
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import (QMatrix4x4, QQuaternion, QVector3D, QFont, QColor)

from models.leaf_click_options import LeafClickOptions
from models.tree_leaf_model import TreeLeafModel


class LookAtTransform(Qt3DCore.QTransform):
    def __init__(self, camera: Qt3DRender.QCamera, parent: QObject = None):
        super().__init__(parent)
        self.camera = camera
        self.target = QVector3D(0, 0, 0)
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
        self.setScale(0.5)


class TreeLeaf(QObject):
    clicked = Signal(LeafClickOptions)

    def __init__(self, parentEntity, camera: Qt3DRender.QCamera, model: TreeLeafModel = None):
        super().__init__()

        self.parentEntity = parentEntity
        self.model = model

        if model is None:
            self.model = TreeLeafModel()

        # region Icon Entity
        self.iconEntity = Qt3DCore.QEntity(self.parentEntity)
        self.iconMesh = Qt3DExtras.QCuboidMesh(self.parentEntity)
        self.iconObjectPicker = Qt3DRender.QObjectPicker(self.parentEntity)
        self.iconMaterial = Qt3DExtras.QPhongMaterial(self.parentEntity)
        color = QColor(0, 0, 0)  # default black
        shine = 10
        if model.isFile():
            color = QColor(50, 130, 246)  # blue
        if model.isDrive():
            color = QColor(128, 128, 128)  # grey
        if model.isFolder():
            color = QColor(255, 201, 14)  # yellow
        self.iconMaterial.setDiffuse(color)
        self.iconMaterial.setAmbient(color)
        # self.iconMaterial.setSpecular(color)
        self.iconMaterial.setShininess(shine)

        self.iconTransform = Qt3DCore.QTransform()
        self.iconTransform.setScale(1.0)

        self.iconEntity.addComponent(self.iconMesh)
        self.iconEntity.addComponent(self.iconObjectPicker)
        self.iconEntity.addComponent(self.iconTransform)
        self.iconEntity.addComponent(self.iconMaterial)

        # endregion

        # region text
        # define the text entity
        self.textEntity = Qt3DCore.QEntity(self.iconEntity)
        self.textMaterial = Qt3DExtras.QPhongMaterial(self.iconEntity)
        self.textMaterial.setDiffuse(QColor(255, 0, 0))

        self.textTransform = LookAtTransform(camera, self.iconEntity)
        self.textTransform.rotationChanged.connect(self.handleTextRotationChanged)
        self.textTransform.scaleChanged.connect(self.handleTextScaleChanged)
        self.textTransform.matrixChanged.connect(self.handleTextRotationMatrixChanged)
        self.textTransform.setScale(0.5)

        self.textMesh = Qt3DExtras.QExtrudedTextMesh(self.iconEntity)
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
        self.iconTransform.setTranslation(p)
        self.textTransform.setTranslation(q)

    def __handleClick(self, event: Qt3DRender.QPickEvent):
        """
        collects click event and emits a signal carrying the click information
        :param event:
        :return:
        """
        opts = LeafClickOptions(self.model, event)
        self.clicked.emit(opts)

    def handleTextRotationChanged(self, rotation: QQuaternion):
        p = self.model.textPosition()
        self.textTransform.setTranslation(p)

    def handleTextRotationMatrixChanged(self):
        p = self.model.textPosition()
        self.textTransform.setTranslation(p)

    def handleTextScaleChanged(self, scale: float):
        p = self.model.textPosition()
        self.textTransform.setTranslation(p)

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
