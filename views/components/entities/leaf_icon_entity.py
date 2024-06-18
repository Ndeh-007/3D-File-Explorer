from PySide6.Qt3DCore import (Qt3DCore)
from PySide6.Qt3DExtras import (Qt3DExtras)

from models.tree_leaf_model import TreeLeafModel
from views.components.entities.base_tree_entity import BaseTreeEntity


class LeafIconEntity(BaseTreeEntity):
    def __init__(self, rootEntity, model: TreeLeafModel):
        super().__init__(rootEntity, model)

        mesh = Qt3DExtras.QCuboidMesh(rootEntity)

        self.setMesh(mesh)

