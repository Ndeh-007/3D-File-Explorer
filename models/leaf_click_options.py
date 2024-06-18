from models.tree_leaf_model import TreeLeafModel
from PySide6.Qt3DRender import Qt3DRender


class LeafClickOptions:
    def __init__(self, leafModel: TreeLeafModel, pickEvent: Qt3DRender.QPickEvent):
        self.leafModel = leafModel
        self.pickEvent = pickEvent
