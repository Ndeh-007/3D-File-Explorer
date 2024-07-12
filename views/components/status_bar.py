import os.path

from PySide6.QtWidgets import QStatusBar, QLabel

from core.utils.helpers import countItemsInDirectory


class VStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.numItemsLabel = QLabel(" 0 items ")
        self.permanentWidget = QLabel("File World    ")

        self.addPermanentWidget(self.permanentWidget)
        self.addWidget(self.numItemsLabel)

        self.setSizeGripEnabled(False)

    def updateNumItems(self, path: str):
        """
        counts items in the provided path and updates the numItemsLabel
        :param path:
        :return:
        """

        if not os.path.exists(path) or os.path.isfile(path):
            return
        count = countItemsInDirectory(path)
        self.numItemsLabel.setText(f" {count} items ")

