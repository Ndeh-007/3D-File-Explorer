import os.path

from PySide6.QtWidgets import QStatusBar, QLabel


class VStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.numItemsLabel = QLabel(" 0 items ")
        self.permanentWidget = QLabel(" FileTree ")

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
        count = self.__countItemsInDirectory(path)
        self.numItemsLabel.setText(f" {count} items ")

    @staticmethod
    def __countItemsInDirectory(path: str):
        """
        Counts the number of items in a directory
        :param path:
        :return:
        """
        try:
            items = os.listdir(path)
            return len(items)
        except FileNotFoundError:
            print(f"The directory {path} does not exist.")
            return 0
        except PermissionError:
            print(f"Permission denied to access the directory {path}.")
            return 0
