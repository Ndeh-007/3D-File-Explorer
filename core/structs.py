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


# region - alert

class AlertDisplayMode(Enum):
    CONSOLE = 0
    NOTIFICATION = 1


class AlertType(Enum):
    ERROR = 0
    SUCCESS = 1
    WARNING = 2
    EVENT = 3


class AlertDisplayType(Enum):
    CONSOLE = 0
    NOTIFICATION = 1


class AlertCode(Enum):
    CUSTOM = "CUSTOM"
# endregion


