from PySide6.Qt3DCore import (Qt3DCore)
from PySide6.Qt3DExtras import (Qt3DExtras)

from core.structs import LeafType


class BaseTreeEntity(Qt3DCore.QEntity):
    def __init__(self, rootEntity: Qt3DCore.QEntity, model: LeafType):
        super().__init__()

        self.__rootEntity = rootEntity
        self.__material = Qt3DExtras.QPhongMaterial(rootEntity)
        self.__mesh = None
        self.__model = model
        self.__entity = None

    def entity(self):
        return self.__entity

    def model(self) -> LeafType:
        return self.__model

    def rootEntity(self):
        return self.__rootEntity

    def material(self):
        return self.__material

    def mesh(self):
        return self.__mesh

    def setMesh(self, mesh):
        self.__mesh = mesh
        self.entity()

    def setMaterial(self, material):
        self.__material = material

    def setModel(self, model):
        self.__model = model

    def setEntity(self, entity):
        self.__entity = entity
