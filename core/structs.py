from enum import Enum


class AppActionTypes(Enum):
    COPY = 0
    PASTE = 1
    MOVE = 2
    DELETE = 3
    BACK = 4
    FORWARD = 5
    UP = 6
    REFRESH = 7
    SETTINGS = 8
    PROPERTIES = 9


class LeafType(Enum):
    FILE = 0
    FOLDER = 1
    DRIVE = 2
    UNSET = 3
    MOUNT = 4