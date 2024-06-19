import os
import platform
import datetime

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTableWidgetItem

from core.structs import LeafType


def get_directory_size(directory_path):
    """
    Calculate the total size of a directory including its subdirectories.

    :param directory_path: Path to the directory
    :return: Total size in bytes
    """
    total_size = 0

    try:
        for entry in os.scandir(directory_path):
            if entry.is_dir(follow_symlinks=False):
                total_size += get_directory_size(entry.path)
            else:
                total_size += entry.stat(follow_symlinks=False).st_size
    except NotADirectoryError:
        return os.path.getsize(directory_path)
    except PermissionError:
        print(f"Permission denied: {directory_path}")
        return 0

    return total_size


def getDirectorProperties(path: str) -> list[list[QTableWidgetItem]]:
    """
    gets the properties of item of the chosen item as an (N,2) arr
    :param path:
    :return:
    """

    if not os.path.exists(path):
        return []
    try:
        size = get_directory_size(path)
        arr = [
            [QTableWidgetItem("Type"), QTableWidgetItem("directory" if os.path.isdir(path) else "file")],
            [QTableWidgetItem("Size"), QTableWidgetItem(f"{size:,} bytes")],
            [QTableWidgetItem("Location"), QTableWidgetItem(path)],
            [QTableWidgetItem("Date modified"),
             QTableWidgetItem(str(datetime.datetime.fromtimestamp(os.path.getmtime(path))))],
        ]
        for items in arr:
            items[0].setFlags(Qt.ItemFlag.ItemIsEnabled)
            items[1].setFlags(Qt.ItemFlag.NoItemFlags)
        return arr
    except OSError as e:
        print("Error encountered", e)
        return []


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


def countItemsInDirectory(path: str) -> int:
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


def openFile(path: str):
    """
    Open a file on system using the default associated application.

    :param path: Path to the file to be opened
    """
    try:
        os.startfile(path)
        print(f"Opening file: {path}")
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to open the file: {e}")
