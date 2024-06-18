import qtawesome
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar, QWidget

from core.structs import AppActionTypes


class PropertiesToolbar(QToolBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        copyAction = QAction(self)
        pasteAction = QAction(self)
        deleteAction = QAction(self)
        moveAction = QAction(self)

        copyAction.setData(AppActionTypes.COPY)
        pasteAction.setData(AppActionTypes.PASTE)
        deleteAction.setData(AppActionTypes.DELETE)
        moveAction.setData(AppActionTypes.MOVE)

        copyIcon = qtawesome.icon("msc.copy")
        deleteIcon = qtawesome.icon("msc.trash")
        moveIcon = qtawesome.icon("msc.move")
        pasteIcon = qtawesome.icon("msc.clippy")

        copyAction.setIcon(copyIcon)
        deleteAction.setIcon(deleteIcon)
        moveAction.setIcon(moveIcon)
        pasteAction.setIcon(pasteIcon)

        self.addAction(copyAction)
        self.addAction(deleteAction)
        self.addAction(moveAction)
        self.addAction(pasteAction)
